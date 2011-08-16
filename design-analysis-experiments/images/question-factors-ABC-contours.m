X = [ 1 1 1 1 1 1 1 1; -1 1 -1 1 -1  1 -1 1; ...
     -1 -1 1 1 -1 -1 1 1; -1 -1 -1 -1 +1 +1 +1 +1]';
X(:,5) = X(:,2) .* X(:,3);
X(:,6) = X(:,2) .* X(:,4);
X(:,7) = X(:,3) .* X(:,4);
X(:,8) = X(:,2) .* X(:,3) .* X(:,4);
y = [72 73 66 87 70 73 67 87]';
inv(X'*X)  % verify that X is orthogonal 
b=inv(X'*X) * X'*y

[A,B] = meshgrid(-2:.2:2, -2:.2:2);
y_hat = b(1) + b(2) .*A + b(3).*B + b(5) .* A .* B;
contour(A, B, y_hat,'LineWidth', 2)
axis equal
xlabel('A [Temperature]', 'FontSize', 14)
ylabel('B [pH]', 'FontSize', 14)
title('Contours of y=conversion for A and B', 'FontSize', 14)
hold on
grid on
plot(-1, -1, 'ko', 'Markersize', 10, 'LineWidth',4)
plot(+1, -1, 'ko', 'Markersize', 10, 'LineWidth',4)
plot(-1, +1, 'ko', 'Markersize', 10, 'LineWidth',4)
plot(+1, +1, 'ko', 'Markersize', 10, 'LineWidth',4)
plot(+1.5, +1.5, 'k*', 'Markersize', 10, 'LineWidth',1)
print -dpng -r200 question-factors-ABC-contours.png