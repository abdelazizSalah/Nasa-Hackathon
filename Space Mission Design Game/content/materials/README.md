# Material sources and rebuild instructions

All maps are bundled with the game; runtime does not download anything.

## NASA imagery

- `earth-blue-marble.png`: original 2048 x 1024 map from [NASA SVS, Blue Marble](https://svs.gsfc.nasa.gov/2915/).
  Direct file: https://svs.gsfc.nasa.gov/vis/a000000/a002900/a002915/bluemarble-2048.png
  Credit: NASA/Goddard Space Flight Center Scientific Visualization Studio; Blue Marble data courtesy of Reto Stockli (NASA/GSFC) and NASA's Earth Observatory.
- `earth-clouds.jpg`: original 2048 x 1024 cloud map from [NASA Earth Observatory, The Blue Marble (2002)](https://science.nasa.gov/earth/earth-observatory/the-blue-marble-true-color-global-imagery-at-1km-resolution/).
  Direct file: https://assets.science.nasa.gov/content/dam/science/esd/eo/content-feature/bluemarble/images/cloud_combined_2048.jpg
  Credit: NASA Goddard Space Flight Center; image by Reto Stockli, enhancements by Robert Simmon.

Downloaded 2026-11-15. The cloud shader derives opacity from the original luminance; these historical composites are decorative and do not show current weather. Ocean highlights, atmosphere and lighting are artistic approximations, not atmospheric/scientific simulation outputs.

NASA media usage: https://www.nasa.gov/nasa-brand-center/images-and-media/
Educational use with attribution; no NASA logo or claim of NASA endorsement is included.

## Original procedural materials

The remaining maps are original project assets: metal, equipment/wall panels, deck plate, thermal foil, solar cells, ceramic, rubber, fabric, optical glass and hazard markings. Rebuild using `python -m game.presentation.materials` from the game directory. This requires only the existing Pillow dependency and preserves both downloaded NASA maps.

Earth maps are 2048 x 1024, and equipment maps are at most 512 x 512. Cached textures, mipmaps and 4x anisotropic filtering reduce repeated loading and surface shimmer. The smooth Earth mesh is built once as a template; each globe/cloud/atmosphere uses an independent copied node because assigning the same Ursina Mesh to multiple entities reparents it.
