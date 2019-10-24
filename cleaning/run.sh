
#python extract.py
#python resize.py

python test2.py --dataroot ./datasets/roadshow --name edge2birds_roadshow --model pix2pix --no_flip --netG unet_256 --preprocess resize --load_size 256 --crop_size 256 --netD n_layers --n_layers_D 3 --batch_size 16 --input_nc 1 --output_nc 3 --dataset_mode twocat --num_classes 8 --class_csv class.csv --num_test 9999 --test --test_mode binary



python train.py --dataroot ./datasets/birds --name edge2birds_augmented_binarized --model pix2pix --no_flip --netG unet_256 --preprocess resize --load_size 256 --crop_size 256 --netD n_layers --n_layers_D 3 --save_latest_freq 34555 --save_epoch_freq 3 --display_id 0 --niter 42 --niter_decay 0 --batch_size 16 --input_nc 1 --output_nc 3 --dataset_mode twocat --print_freq 1000 --update_html_freq 1000 --num_classes 8 --class_csv class.csv

python test.py --dataroot ./datasets/birds --name edge2birds_augmented_binarized --model pix2pix --no_flip --netG unet_256 --preprocess resize --load_size 256 --crop_size 256 --netD n_layers --n_layers_D 3 --batch_size 16 --input_nc 1 --output_nc 3 --dataset_mode twocat --num_classes 8 --class_csv class.csv --num_test 9999

python test.py --dataroot ./datasets/birds_blue --name edge2birds_augmented_binarized --model pix2pix --no_flip --netG unet_256 --preprocess resize --load_size 256 --crop_size 256 --netD n_layers --n_layers_D 3 --batch_size 16 --input_nc 1 --output_nc 3 --dataset_mode twocat --num_classes 8 --class_csv class.csv --num_test 9999

python test.py --dataroot ./datasets/birds_drawn --name edge2birds_augmented_binarized --model pix2pix --no_flip --netG unet_256 --preprocess resize --load_size 256 --crop_size 256 --netD n_layers --n_layers_D 3 --batch_size 16 --input_nc 1 --output_nc 3 --dataset_mode twocat --num_classes 8 --class_csv class.csv --num_test 9999 --test --test_mode binary


python train.py --dataroot ./datasets/birds_augmented --name edge2birds_augmented_classless --model pix2pix --no_flip --netG unet_256 --preprocess resize --load_size 256 --crop_size 256 --netD n_layers --n_layers_D 3 --save_latest_freq 36843 --save_epoch_freq 3 --display_id 0 --niter 42 --niter_decay 0 --batch_size 16 --input_nc 1 --output_nc 3 --dataset_mode twocat --print_freq 1000 --update_html_freq 1000 --num_classes 7 --class_csv class.csv

python test.py --dataroot ./datasets/birds_augmented --name edge2birds_augmented_classless --model pix2pix --no_flip --netG unet_256 --preprocess resize --load_size 256 --crop_size 256 --netD n_layers --n_layers_D 3 --batch_size 16 --input_nc 1 --output_nc 3 --dataset_mode twocat --num_classes 7 --class_csv class.csv --num_test 9999


python train.py --dataroot ./datasets/birds_augmented --name edge2birds_augmented3 --model pix2pix --no_flip --netG unet_256 --preprocess resize --load_size 256 --crop_size 256 --netD n_layers --n_layers_D 3 --save_latest_freq 36843 --save_epoch_freq 3 --display_id 0 --niter 42 --niter_decay 0 --batch_size 16 --input_nc 1 --output_nc 3 --dataset_mode twocat --print_freq 1000 --update_html_freq 1000 --num_classes 7 --class_csv class.csv

python test.py --dataroot ./datasets/birds_augmented --name edge2birds_augmented3 --model pix2pix --no_flip --netG unet_256 --preprocess resize --load_size 256 --crop_size 256 --netD n_layers --n_layers_D 3 --batch_size 16 --input_nc 1 --output_nc 3 --dataset_mode twocat --num_classes 7 --class_csv class.csv --num_test 9999

python train.py --dataroot ./datasets/birds_augmented --name edge2birds_augmented2 --model pix2pix --no_flip --netG unet_256 --preprocess resize --load_size 256 --crop_size 256 --netD n_layers --n_layers_D 3 --save_latest_freq 36843 --save_epoch_freq 3 --display_id 0 --niter 42 --niter_decay 0 --batch_size 8 --input_nc 1 --output_nc 3 --dataset_mode twocat --print_freq 1000 --update_html_freq 1000 --num_classes 7 --class_csv class.csv --continue_train --epoch_count 8

python test.py --dataroot ./datasets/birds_augmented --name edge2birds_augmented2 --model pix2pix --no_flip --netG unet_256 --preprocess resize --load_size 256 --crop_size 256 --netD n_layers --n_layers_D 3 --batch_size 8 --input_nc 1 --output_nc 3 --dataset_mode twocat --num_classes 7 --class_csv class.csv --num_test 9999


python createwhitelist.py "D:\Documents\pytorch-CycleGAN-and-pix2pix\datasets\birds\images\train"

python whitelist.py "D:\Documents\pix2pix\datasets\birds\256x256 edges\backgroundless_edges" "D:\Documents\pix2pix\datasets\birds\256x256 edges\new_backgroundless_edges"
python whitelist.py "D:\Documents\pix2pix\datasets\birds\256x256 images\backgroundless_images" "D:\Documents\pix2pix\datasets\birds\256x256 images\new_backgroundless_images"

cd ..

python datasets/combine_A_and_B.py --fold_A datasets/Macaws/contoured_cut --fold_B datasets/Macaws/contoured_outlines --fold_AB datasets/Macaws/contoured-cut-outlines

python train.py --dataroot ./datasets/birds --name edge2birds --model pix2pix --no_flip --netG unet_256 --load_size 256 --crop_size 256 --netD n_layers --n_layers_D 3 --save_latest_freq 547 --save_epoch_freq 20 --display_id 0 --niter 200 --niter_decay 0 --batch_size 1 --input_nc 1 --output_nc 3 --dataset_mode twocat --print_freq 100 --update_html_freq 100 --num_classes 7 --class_csv class.csv

python test.py --dataroot ./datasets/birds --name edge2birds --model pix2pix --no_flip --netG unet_256 --load_size 256 --crop_size 256 --netD n_layers --n_layers_D 3 --batch_size 1 --input_nc 1 --output_nc 3 --dataset_mode twocat --num_classes 7 --class_csv class.csv

python train.py --dataroot ./datasets/birds --name edge2birds --model pix2pix --preprocess resize --load_size 128 --crop_size 128 --no_flip --netG unet_128 --netD n_layers --n_layers_D 3 --save_latest_freq 35732 --save_epoch_freq 3 --display_id 0 --niter 48 --niter_decay 0 --batch_size 16 --input_nc 1 --output_nc 3 --dataset_mode twocat --print_freq 1000 --update_html_freq 1000
python test.py --dataroot ./datasets/birds --name edge2birds --model pix2pix --preprocess resize --load_size 128 --crop_size 128 --no_flip --netG unet_128 --netD n_layers --n_layers_D 3 --input_nc 1 --output_nc 3 --batch_size 16 --dataset_mode twocat --num_test 9999

python train.py --dataroot ./datasets/birds --name edge2birds --model pix2pix --direction BtoA --preprocess resize --load_size 64 --crop_size 64 --no_flip --netG unet_64 --netD n_layers --n_layers_D 2 --save_latest_freq 490 --save_epoch_freq 20 --display_id 0 --niter 200 --niter_decay 0 --batch_size 4 --input_nc=1
python test.py --dataroot ./datasets/birds --name edge2birds --model pix2pix --direction BtoA --preprocess resize --load_size 64 --crop_size 64 --no_flip --netG unet_64 --netD n_layers --n_layers_D 2 --input_nc=1

python train.py --dataroot ./datasets/birds --name edge2birds --model pix2pix --direction BtoA --preprocess resize --load_size 64 --crop_size 64 --no_flip --netG unet_64 --netD n_layers --n_layers_D 2 --save_latest_freq 495 --save_epoch_freq 20 --display_id 0 --niter 200 --niter_decay 0 --batch_size 4  --continue_train --epoch_count 61

# Epoch 179 - Rmb to add
python train.py --dataroot ./datasets/birds --name edge2birds --model pix2pix --direction BtoA --preprocess resize --load_size 64 --crop_size 64 --no_flip --netG unet_64 --netD n_layers --n_layers_D 2 --save_latest_freq 1334 --save_epoch_freq 20 --display_id 0 --niter 200 --niter_decay 0 --batch_size 4 --continue_train --epoch_count 179

# Epoch 79
python train.py --dataroot ./datasets/birds --name edge2birds --model pix2pix --direction BtoA --preprocess resize --load_size 64 --crop_size 64 --no_flip --netG unet_64 --netD n_layers --n_layers_D 2 --save_latest_freq 1654 --save_epoch_freq 20 --display_id 0 --niter 200 --niter_decay 0 --batch_size 16 --continue_train --epoch_count 79
python test.py --dataroot ./datasets/birds --name edge2birds --model pix2pix --direction BtoA --preprocess resize --load_size 64 --crop_size 64 --no_flip --netG unet_64 --netD n_layers --n_layers_D 2
