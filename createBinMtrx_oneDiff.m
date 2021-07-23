function B_out = createBinMtrx_oneDiff(n)

oldB = false(1,n);

for kk = 1:n
    newB = flipud(oldB);
    newB(:,kk) = ~newB(:,kk);
    oldB = [oldB;newB];
end
B_out = oldB;