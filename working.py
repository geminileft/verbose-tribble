import os

header_lines = []
all_vertices = []

def output_obj_data(name, vertices, faces, obj_face_extra):
    output_lines = []
    for line in header_lines:
        output_lines.append(line)
    print('object name: {}'.format(name))
    unsorted_vertices = list(vertices)
    unsorted_vertices.sort()
    mapped_vertices = {}
    i = 1
    sum_x = 0.0
    sum_z = 0.0

    for vertex in unsorted_vertices:
        line = all_vertices[vertex - 1]
        coords = line.split(' ')[1:]
        sum_x += float(coords[0])
        sum_z += float(coords[2])
        i  += 1

    mid_x = sum_x / (i - 1)
    mid_z = sum_z / (i - 1)

    off_x = 0 - mid_x
    off_z = 0 - mid_z

    i = 1
    for vertex in unsorted_vertices:
        line = all_vertices[vertex - 1]
        coords = line.split(' ')[1:]
        x = float(coords[0]) + off_x
        y = float(coords[1])
        z = float(coords[2]) + off_z
        output_lines.append('v {} {} {}'.format(x, y, z))
        mapped_vertices[vertex] = i
        i += 1

    face_index = 1
    for face_data in faces:
        if face_index in obj_face_extra:
            for face_extra in obj_face_extra[face_index]:
                output_lines.append(face_extra)
        face_index += 1
        new_face_data = []
        for face_vertex in face_data:
            vertex_index = int(face_vertex)
            new_vertex_index = str(mapped_vertices[vertex_index])
            new_face_data.append(new_vertex_index)
        output_lines.append('{} {}'.format('f', ' '.join(new_face_data)))
    with open('./{}.obj'.format(name), 'w') as f:
        f.writelines(['{}{}'.format(line, os.linesep) for line in output_lines] )
        f.close()
    print("done with obj data")


filename = "/Users/dev/Downloads/Blender Nature Asset/BlenderNatureAsset.obj"

with open(filename) as f:
    lines = f.read().splitlines()

obj_name = None
obj_faces = []
obj_face_extra = {}
obj_vertices = set()
face_index = 1
for line in lines:
    fields = line.split(" ")
    field_type = fields[0]
    if field_type == '#':
        header_lines.append(line)
        print('Comment field')
    elif field_type == 'mtllib':
        header_lines.append(line)
        print('{} {}'.format(fields[0],fields[1]))
    elif field_type == 'usemtl' or field_type == 's':
        if face_index not in obj_face_extra:
            extras = []
        else:
            extras = obj_face_extra[face_index]
        extras.append(line)
        obj_face_extra[face_index] = extras
        print('{} {}'.format(fields[0],fields[1]))
    elif field_type == 'o':
        if obj_name is not None:
            output_obj_data(obj_name, obj_vertices, obj_faces, obj_face_extra)
        obj_name = fields[1]
        obj_vertices.clear()
        obj_faces.clear()
        obj_face_extra.clear()
        face_index = 1
        print('start of obj definition: {}'.format(line))
    elif field_type == 'f':
        print('face: {}'.format(line))
        obj_faces.append(fields[1:])
        for face_vertex_index in fields[1:]:
            obj_vertices.add(int(face_vertex_index))
        face_index += 1
    elif field_type == 'v':
        all_vertices.append(line)
    else:
        print("field type: {}".format(field_type))

