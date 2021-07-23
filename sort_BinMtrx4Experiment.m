% n = 8;
% b_show = true;
% bin_matrix = myAllBinPerms(n);
% bin_matrix = bin_matrix(2:end,:);

function sorted_binMtrx = sort_BinMtrx4Experiment(bin_matrix, o_show, b_rand)
if nargin < 2
    o_show = 0;
end
if nargin < 3
    b_rand = false;
end

sz_binM = size(bin_matrix,1);
% if b_rand
%     bin_matrix = bin_matrix(randperm(sz_binM),:); %%% randomly permute rows of matrix
% end

af_remRow = @(M,n) M([1:(n-1) (n+1):end],:);

k = 1;
new_row = bin_matrix(k,:);
bin_matrix = af_remRow(bin_matrix,k);
sorted_binMtrx = [];

if o_show >0
    h_fig = figure(33);
    subplot(221);
    h_im1 = imagesc(sorted_binMtrx);
    subplot(222);
    h_im2 = imagesc(bin_matrix);
    subplot(313);
    h_pl1 = plot(1,nan);
end

while sz_binM >= 1
    sorted_binMtrx = [sorted_binMtrx; new_row];
    sel_crit = sum(abs(bin_matrix-sorted_binMtrx(end,:)),2);
    k = find(sel_crit == min(sel_crit),1);
    new_row = bin_matrix(k,:);
    if o_show > 1
        diff_bin_matrix = bin_matrix;
        diff_bin_matrix(k,:) = 3*diff_bin_matrix(k,:);
        v_elMoved = sum(abs(diff(sorted_binMtrx,1)),2);
        set(h_im1, 'CData', sorted_binMtrx);
        set(h_im2, 'CData', diff_bin_matrix);
        set(h_pl1, 'XData', 1:length(v_elMoved), 'YData', v_elMoved);
        drawnow;
        %     pause(0.1);
    end
    
    bin_matrix = af_remRow(bin_matrix,k);
    sz_binM = size(bin_matrix,1);
    
    if b_rand
        bin_matrix = bin_matrix(randperm(sz_binM),:); %%% randomly permute rows of matrix
    end
end

sorted_binMtrx = [sorted_binMtrx; new_row];
if o_show > 0
    v_elMoved = sum(abs(diff(sorted_binMtrx,1)),2);
    set(h_im1, 'CData', sorted_binMtrx);
    set(h_im2, 'CData', bin_matrix);
    set(h_pl1, 'XData', 1:length(v_elMoved), 'YData', v_elMoved);
end
end