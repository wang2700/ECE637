close all
h = zeros(9, 9) + 1/81;

colormap(parula(64))
[H, f1, f2] = freqz2(h);
f1 = f1 * pi;
f2 = f2 * pi;
mesh(f1, f2, abs(H))
axis ([-pi pi -pi pi 0 1])
xlabel('f_1 (rad)')
ylabel('f_2 (rad)')
zlabel('magnitude')
title('Frequency Response of FIR Low Pass Filter')