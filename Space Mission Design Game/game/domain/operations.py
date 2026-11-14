"""Time-stamped trajectory geometry and resource simulation in consistent km/s units."""
import math

R=6378.137
OMEGA=7.292115e-5

def geometry(row):
    t=row[0]; x,y,z=row[2:5]; radius=math.sqrt(x*x+y*y+z*z)
    # Epoch-relative Earth-fixed station at equator/longitude zero (teaching alignment).
    station=(R*math.cos(OMEGA*t),R*math.sin(OMEGA*t),0)
    delta=[p-s for p,s in zip((x,y,z),station)]
    distance=math.sqrt(sum(v*v for v in delta))
    elevation=sum(a*b for a,b in zip(delta,station))/(max(distance,1e-9)*R)
    contact=elevation>math.sin(math.radians(5))
    # Cylindrical Earth shadow, constant Sun along +X for this short educational run.
    eclipse=x<0 and y*y+z*z<R*R
    target=(R*math.cos(OMEGA*t),R*math.sin(OMEGA*t),0)
    visible=sum(a*b for a,b in zip((x,y,z),target))/(radius*R)>math.cos(math.radians(35))
    return {'contact':contact,'eclipse':eclipse,'target_visible':visible,'radius_km':radius}

def simulate(catalog,design,rows,targeted=True):
    from game.domain.design import selected
    c=selected(catalog,design); base=catalog['scenario']; battery=c['power']['battery_wh']
    storage=delivered=generated=lost=unserved=0.; frames=[]
    for i,row in enumerate(rows):
        g=geometry(row); dt=(rows[i+1][0]-row[0]) if i+1<len(rows) else 0
        observe=g['target_visible'] and not g['eclipse'] and (not targeted or generated<120)
        load=base['baseline_power_w']+(c['sensor']['power_w'] if observe else 0)+(c['radio']['power_w'] if g['contact'] else 0)
        energy=(0 if g['eclipse'] else c['power']['generation_w'])*dt/3600
        demand=load*dt/3600; short=max(0,demand-battery-energy); unserved+=short
        fraction=1-short/demand if demand else 1
        battery=max(0,min(c['power']['battery_wh'],battery+energy-demand))
        data=c['sensor']['data_mb_min']*dt/60*fraction if observe else 0
        if targeted: data=min(data,max(0,120-generated))
        generated+=data; lost+=max(0,storage+data-base['storage_mb']); storage=min(base['storage_mb'],storage+data)
        sent=min(storage,c['radio']['downlink_mb_min']*dt/60*fraction) if g['contact'] else 0
        storage-=sent; delivered+=sent
        frames.append({'t':row[0],'position':row[2:5],**g,'battery_wh':battery,'storage_mb':storage,'delivered_mb':delivered})
    passed=delivered>=60 and unserved<1e-6 and lost<1e-6
    return {'passed':passed,'delivered_mb':delivered,'generated_mb':generated,'lost_mb':lost,
            'unserved_wh':unserved,'required_mb':60,'frames':frames,
            'reason':'Delivery target met with no energy shortage or storage loss.' if passed else
            ('Battery energy ran out; increase power package or revise the design.' if unserved>1e-6 else
             'Storage overflowed; reduce sensor data or improve downlink.' if lost>1e-6 else 'Not enough data reached the station during contacts.')}
