close all
size = 64;
u_vec = linspace(-pi, pi, size);
v_vec = linspace(-pi, pi, size);
H = zeros(size, size);
ind = 1;
for u = u_vec
    H(ind, :) = abs(0.01./(1-0.9*exp(-1i*u)-0.9*exp(-1i*v_vec)+0.81*exp(-1i*u-1i*v_vec)));
    ind = ind + 1;
end
mesh(u_vec, v_vec, H);
xlabel('u')
ylabel('v')
zlabel('Magnitude')
xlim([-pi, pi])
ylim([-pi, pi])
title('Frequency Response of the IIR filter')

%calculate point spread function
figure
in = zeros(256,256);
in(127, 127) = 1;
h = zeros(256, 256);
for i = 1:256
    for j = 1:256
        y = 0.01*in(i,j);
        if (i-1) > 0
            y = y + 0.9 * h(i-1, j);
        end
        if (j-1) > 0
            y = y + 0.9 * h(i, j-1);
        end
        if (i-1) > 0 && (j-1) > 0
            y = y - 0.81 * h(i-1, j-1);
        end
        h(i,j) = y;
    end
end
imshow(uint8(255*100*h))
imwrite(uint8(255*100*h), 'h_out.png');
imwrite(uint8(255*100*h), 'h_out.tif', 'tif', 'Compression', 'none');