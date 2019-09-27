
#python extract.py
#python resize.py

cd ..

python datasets/combine_A_and_B.py --fold_A datasets/Macaws/background --fold_B datasets/Macaws/outlines --fold_AB datasets/Macaws/combined
