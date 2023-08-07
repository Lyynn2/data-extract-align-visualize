
% hrs = [35.71, 31.25, 25.97, 35.61, 35.09, 32.55];
good_hr_ranges = [
        1570 1605 1594.62 1596.54 1587.64 1585.96 1 1   % (1587.64 - 1585.96)/1 --> 35.71, (1596.54 - 1594.62)/1 --> 31.25
        1679 1692 1685.76 1681.14 nan nan         2 nan % (1685.76 - 1681.14)/2 --> 25.97
        5516 5544 5533.96 5520.48 5537.38 5539.09 7 1   % (5533.96 - 5520.48)/8 --> 35.61, (5539.09 - 5537.38)/1 --> 35.09
        1595 1604 1596.49 1602.02 nan nan         3 nan % (1602.02 - 1596.49)/3 --> 32.55
        ];
good_zoomin_ranges = [
%     5313.4 5314.8 % 3 back to back
    1595 1604
    1658.2 1661.2 % 1 zoom-in
    1630.7 1632.1 % 1 zoom-in
    %5507 5518
    5527.5 5529
    ];
ecg_filter_passband = [2, 100];

ecg_filtered = bandpass(ecg, ecg_filter_passband, ecg_Fs);
figure(60); clf;
for i = 1:size(good_hr_ranges, 1)
    subplot(size(good_hr_ranges, 1), 1, i);
    start_index = find(ecg_t >= good_hr_ranges(i, 1), 1, 'first');
    end_index = find(ecg_t <= good_hr_ranges(i, 2), 1, 'last');
    ecg_demean = ecg - mean(ecg);
    myplot(ecg_t(start_index:end_index), ecg(start_index:end_index) - mean(ecg(start_index:end_index)), 'c', 'linewidth', 1);
    myplot(ecg_t(start_index:end_index), ecg_filtered(start_index:end_index) - mean(ecg_filtered(start_index:end_index)), 'r');
    d_colors = {'k', 'm', 'g'};
    title_txt = 'Estimated Heart Rates:  ';
    d_indexes = [];
    for d = 3:2:(size(good_hr_ranges, 2)-2)
        d_index_start = find(abs(ecg_t - good_hr_ranges(i, d)) == min(abs(ecg_t - good_hr_ranges(i, d))), 1, 'first');
        d_index_end = find(abs(ecg_t - good_hr_ranges(i, d+1)) == min(abs(ecg_t - good_hr_ranges(i, d+1))), 1, 'first');
        if ~isempty(d_index_end)
            myplot(ecg_t([d_index_start d_index_end]), max(ylim)*0.9*[1 1], 'o-', 'color', d_colors{round((d-3+1)/2)}, 'markersize', 8);
            d_indexes(end+1) = d_index_start;
            d_indexes(end+1) = d_index_end;
        end
    end
    for d = 1:2:(length(d_indexes))
        num_periods = good_hr_ranges(i, 7+floor(d/2));
        duration_s = abs((ecg_t(d_indexes(d)) - ecg_t(d_indexes(d+1))));
        hr = 60/duration_s*num_periods;
        title_txt = sprintf('%s%0.1f  ', title_txt, hr);
    end
    title(title_txt);
end
xlabel('Time Since Start [seconds]');
sgtitle('Roger''s Heart Rate!!!! 🐳💓');

figure(61); clf;
for i = 1:size(good_zoomin_ranges, 1)
    subplot(size(good_zoomin_ranges, 1), 1, i);
    start_index = find(ecg_t >= good_zoomin_ranges(i, 1), 1, 'first');
    end_index = find(ecg_t <= good_zoomin_ranges(i, 2), 1, 'last');
    myplot(ecg_t(start_index:end_index), ecg(start_index:end_index) - mean(ecg(start_index:end_index)), 'c', 'linewidth', 1);
    myplot(ecg_t(start_index:end_index), ecg_filtered(start_index:end_index) - mean(ecg_filtered(start_index:end_index)), 'r');
end
sgtitle('More of Roger''s Heartbeats!!!! 🐳💓');
xlabel('Time Since Start [seconds]');

figure(62); clf;
for i = 3
    start_index = find(ecg_t >= good_zoomin_ranges(i, 1), 1, 'first');
    end_index = find(ecg_t <= good_zoomin_ranges(i, 2), 1, 'last');
    myplot(ecg_t(start_index:end_index), ecg(start_index:end_index) - mean(ecg(start_index:end_index)), 'c', 'linewidth', 1);
    myplot(ecg_t(start_index:end_index), ecg_filtered(start_index:end_index) - mean(ecg_filtered(start_index:end_index)), 'r');
end
xlabel('Time Since Start [seconds]');
title('Roger''s Heartbeat!!!! 🐳💓');


