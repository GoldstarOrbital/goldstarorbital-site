# Third-party assets

- Three.js 0.186.1: https://github.com/mrdoob/three.js — MIT license, copied in assets/THREE-LICENSE.txt. Bundled into game.js.
- Earth color texture: Three.js r160 example asset, https://github.com/mrdoob/three.js/blob/r160/examples/textures/planets/earth_atmos_2048.jpg. Downloaded unchanged into assets/earth.jpg, then embedded by the build. Distributed from the Three.js example repository; retained with its project attribution.
- esbuild: development-only build dependency, MIT license in its installed package.
- Ship, station, hull panel textures, interface and pixel graphics are generated locally by this project.

- Mars map: NASA 3D Resources, `Images and Textures/Mars/Mars.jpg`, https://github.com/nasa/NASA-3D-Resources/tree/master/Images%20and%20Textures/Mars. Downloaded unchanged and embedded in the game.
- Asteroid surface: NASA 3D Resources Phobos map, `Images and Textures/Mars - Phobos/Mars - Phobos.jpg`, https://github.com/nasa/NASA-3D-Resources/tree/master/Images%20and%20Textures/Mars%20-%20Phobos. Used as a color and relief reference on fictional asteroid meshes; this does not represent accurate Phobos geometry.
- NASA's repository describes these resources as free and without copyright: https://github.com/nasa/NASA-3D-Resources. Usage guidelines: https://www.nasa.gov/nasa-brand-center/images-and-media/. No NASA endorsement is implied.

## NASA 3D Resources

Spacecraft and asteroid models in `assets/models/` come from NASA 3D Resources
(https://github.com/nasa/NASA-3D-Resources), published by NASA as free and
without copyright: International Space Station, Mars Reconnaissance Orbiter,
TDRS, Landsat 8, CALIPSO, Deep Space 1, Aqua, CloudSat, and asteroid 101955
Bennu (1999 RQ36). Use follows NASA's media usage guidelines
(https://www.nasa.gov/nasa-brand-center/images-and-media). NASA does not
endorse this game, and no NASA insignia or logos are used.

## Draco decoder

`assets/draco/` contains the Google Draco mesh decoder (Apache License 2.0) as
distributed with three.js, used to decompress the NASA models.

## Fonts

DM Sans and Space Mono, SIL Open Font License 1.1 (licence texts in
`assets/fonts/`).

The Aegis orbital interceptor is original project geometry and materials. NASA spacecraft models continue to be used for the station and support network. Mars surface detail beyond the source colour map is a stylized rendering treatment, not an elevation dataset.
