from PIL import Image

changes_im = Image.open('/bot/pfpgups/tmp/changes.png')
(width, height) = changes_im.size
frame = changes_im.crop(((310, 696, 1008, height - 550)))
frame.save('/bot/pfpgups/tmp/changes_frame.png')
changes_im1 = Image.open('/bot/pfpgups/tmp/changes_frame.png')
(width_frame, height_frame) = changes_im1.size
part1 = changes_im1.crop(((0, 0, width_frame, 1231)))
part1.save('/bot/pfpgups/tmp/changes_part1.png')
changes_im2 = Image.open('/bot/pfpgups/tmp/changes_frame.png')
part2 = changes_im2.crop(((0, 1231, width_frame, height_frame)))
part2.save('/bot/pfpgups/tmp/changes_part2.png')


