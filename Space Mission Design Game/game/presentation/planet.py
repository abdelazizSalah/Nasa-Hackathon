"""Shared, smoothly shaded Earth with an offline NASA map and subtle atmosphere."""
import math
from copy import deepcopy
from functools import lru_cache
from ursina import Entity,Mesh,Shader,color
from game.presentation.materials import surface

VERTEX='''#version 150
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;
uniform mat4 p3d_ViewMatrixInverse;
in vec4 p3d_Vertex;
in vec3 p3d_Normal;
in vec2 p3d_MultiTexCoord0;
out vec2 uv;
out vec3 normal_world;
out vec3 to_camera;
void main() {
    gl_Position=p3d_ModelViewProjectionMatrix*p3d_Vertex;
    uv=p3d_MultiTexCoord0;
    normal_world=normalize(transpose(inverse(mat3(p3d_ModelMatrix)))*p3d_Normal);
    to_camera=p3d_ViewMatrixInverse[3].xyz-(p3d_ModelMatrix*p3d_Vertex).xyz;
}
'''
earth_shader=Shader(name='mission_earth',language=Shader.GLSL,vertex=VERTEX,fragment='''#version 150
uniform sampler2D p3d_Texture0;
uniform vec4 p3d_ColorScale;
in vec2 uv;
in vec3 normal_world;
in vec3 to_camera;
out vec4 fragColor;
void main() {
    vec4 tex=texture(p3d_Texture0,uv)*p3d_ColorScale;
    vec3 n=normalize(normal_world);
    vec3 light=normalize(vec3(-.6,.7,-1.0));
    float daylight=max(0.,dot(n,light));
    float ocean=step(tex.r*1.3,tex.b)*step(tex.g,tex.b);
    float glint=pow(max(0.,dot(n,normalize(light+normalize(to_camera)))),48.)*.3*ocean;
    fragColor=vec4(tex.rgb*(.22+daylight*.78)+vec3(.7,.85,1.)*glint,tex.a);
}
''')
cloud_shader=Shader(name='mission_clouds',language=Shader.GLSL,vertex=VERTEX,fragment='''#version 150
uniform sampler2D p3d_Texture0;
in vec2 uv;
in vec3 normal_world;
out vec4 fragColor;
void main() {
    float density=texture(p3d_Texture0,uv).r;
    float daylight=max(0.,dot(normalize(normal_world),normalize(vec3(-.6,.7,-1.0))));
    fragColor=vec4(vec3(.3+daylight*.7),pow(density,1.4)*.85);
}
''')
atmosphere_shader=Shader(name='mission_atmosphere',language=Shader.GLSL,vertex=VERTEX,fragment='''#version 150
in vec3 normal_world;
in vec3 to_camera;
out vec4 fragColor;
void main() {
    float rim=pow(1.-max(0.,dot(normalize(normal_world),normalize(to_camera))),3.5);
    fragColor=vec4(.18,.5,1.,rim*.38);
}
''')

@lru_cache(maxsize=1)
def _globe_source():
    vertices=[];normals=[];uvs=[];triangles=[]
    segments=96;rings=48
    for row in range(rings+1):
        v=row/rings;latitude=(v-.5)*math.pi
        for col in range(segments+1):
            u=col/segments;longitude=(u-.5)*math.tau
            n=(math.cos(latitude)*math.sin(longitude),math.sin(latitude),math.cos(latitude)*math.cos(longitude))
            vertices.append(tuple(c*.5 for c in n));normals.append(n);uvs.append((1-u,v))
    for row in range(rings):
        for col in range(segments):
            a=row*(segments+1)+col;b=a+1;c=a+segments+2;d=c-1
            # Ursina uses a left-handed coordinate system (clockwise front faces).
            triangles.extend(((a,c,b),(a,d,c)))
    return Mesh(vertices=vertices,triangles=triangles,normals=normals,uvs=uvs)

def globe_mesh():
    # Ursina reparents Mesh instances on assignment: each visible layer needs its own node.
    return deepcopy(_globe_source())

def earth(**kwargs):
    globe=Entity(model=globe_mesh(),texture=surface('earth-blue-marble'),color=color.white,
                 shader=earth_shader,**kwargs)
    globe.rotation_y=180
    globe.clouds=Entity(parent=globe,model=globe_mesh(),texture=surface('earth-clouds.jpg'),
                        color=color.white,scale=1.008,shader=cloud_shader)
    globe.clouds.setDepthWrite(False)
    globe.atmosphere=Entity(parent=globe,model=globe_mesh(),scale=1.018,shader=atmosphere_shader)
    globe.atmosphere.setTransparency(True);globe.atmosphere.setDepthWrite(False)
    return globe
