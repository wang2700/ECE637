close all
h = ones(5, 5) * 1/25;

colormap(parula(64))
[H, f1, f2] = freqz2(h);
f1 = f1 * pi;
f2 = f2 * pi;
mesh(f1, f2, abs(H))
axis ([-pi pi -pi pi 0 1])
xlabel('u')
ylabel('v')
zlabel('magnitude')
title('Frequency Response of FIR Low Pass Filter')

figure
delta = zeros(5,5);
delta(3,3) = 1;
lambda = 1.5;
g = delta + lambda .* (delta - h);
[G, f1, f2] = freqz2(g);
f1 = f1 * pi;
f2 = f2 * pi;
mesh(f1, f2, abs(G))
axis ([-pi pi -pi pi 1 3])
xlabel('u')
ylabel('v')
zlabel('magnitude')
title('Frequency Response of FIR Sharpening Filter')