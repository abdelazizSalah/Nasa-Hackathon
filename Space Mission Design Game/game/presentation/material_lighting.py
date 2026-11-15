"""Small directional material shader with tiled UVs and restrained highlights."""
from ursina import Shader,Vec2

material_shader=Shader(name='mission_material',language=Shader.GLSL,vertex='''#version 150
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;
uniform mat4 p3d_ViewMatrixInverse;
uniform vec2 texture_scale;
uniform vec2 texture_offset;
in vec4 p3d_Vertex;
in vec3 p3d_Normal;
in vec2 p3d_MultiTexCoord0;
out vec2 uv;
out vec3 normal_world;
out vec3 to_camera;
void main() {
    gl_Position=p3d_ModelViewProjectionMatrix*p3d_Vertex;
    uv=p3d_MultiTexCoord0*texture_scale+texture_offset;
    normal_world=normalize(transpose(inverse(mat3(p3d_ModelMatrix)))*p3d_Normal);
    to_camera=p3d_ViewMatrixInverse[3].xyz-(p3d_ModelMatrix*p3d_Vertex).xyz;
}
''',fragment='''#version 150
uniform sampler2D p3d_Texture0;
uniform vec4 p3d_ColorScale;
in vec2 uv;
in vec3 normal_world;
in vec3 to_camera;
out vec4 fragColor;
void main() {
    vec4 tex=texture(p3d_Texture0,uv)*p3d_ColorScale;
    vec3 n=normalize(normal_world),light=normalize(vec3(-.4,1.,-.6));
    float diffuse=max(0.,dot(n,light));
    float spec=pow(max(0.,dot(n,normalize(light+normalize(to_camera)))),32.)*.10;
    fragColor=vec4(tex.rgb*(.42+.58*diffuse)+vec3(spec),tex.a);
}
''',default_input={'texture_scale':Vec2(1,1),'texture_offset':Vec2(0,0)})
