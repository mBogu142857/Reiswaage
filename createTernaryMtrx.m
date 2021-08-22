function T_out = createTernaryMtrx(n)

T_old = (-1:1)';
for ii = 1:n-1
    T_new = [-ones(size(T_old,1),1), T_old;...
        zeros(size(T_old,1),1), T_old;...
        ones(size(T_old,1),1), T_old];
    T_old = T_new;
end
T_out = T_old;
end