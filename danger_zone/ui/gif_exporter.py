import os
import shutil

import imageio
import pyglet


class GifExporter:
    FRAME_DIRECTORY = 'gif_frames'

    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.current_frame = 0
        self.file_names = []

        if not os.path.exists(GifExporter.FRAME_DIRECTORY):
            os.makedirs(GifExporter.FRAME_DIRECTORY)
        else:
            shutil.rmtree(GifExporter.FRAME_DIRECTORY)

    def save_frame(self):
        image_path = os.path.join(GifExporter.FRAME_DIRECTORY, 'frame-{}.png'.format(self.current_frame))
        pyglet.image.get_buffer_manager().get_color_buffer().save(image_path)

        self.file_names.append(image_path)

        self.current_frame += 1

        return self.current_frame <= self.num_frames

    def export(self):
        images = []
        for file_name in self.file_names:
            images.append(imageio.imread(file_name))

        kargs = {'duration': 1 / 30}
        imageio.mimsave('danger-zone-export.gif', images, 'GIF', **kargs)

        # Clean up frame directory
        shutil.rmtree(GifExporter.FRAME_DIRECTORY)

        print('Successfully exported GIF animation to this directory!')
        print('Result was saved to "danger-zone-export.gif".')
