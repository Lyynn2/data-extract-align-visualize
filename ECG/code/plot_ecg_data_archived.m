
% Testing on the stand-alone Pi in Stata
% data_dir = 'P:/MIT/Lab/Whales/ECG/data/2022-08-01_2 testing ecg board pi';
% filepath = sprintf('%s/2022-08-01_16-08-15_ecg_log.csv', data_dir);

% Testing on the Pi integrated with the tag at Harvard.
data_dir = 'P:/MIT/Lab/Whales/ECG/data/2022-08-01_3 testing ecg board tag pi';
% filepath = sprintf('%s/2022-08-01_23-12-11_ecg_log_goodTest_touchGround.csv', data_dir);
% filepath = sprintf('%s/2022-08-01_23-29-12_ecg_log_goodTest_touchGround-move-disconnect-sit.csv', data_dir);
filepath = sprintf('%s/2022-08-01_23-42-00_ecg_log_goodTest_touchGround-move-disconnect-sit.csv', data_dir);
% filepath = sprintf('%s/2022-08-02_00-39-46_ecg_log_goodTest_touchGroundLate-move-releaseGround-disconnect.csv', data_dir);

filepath = 'P:/MIT/Lab/Whales/ECG/data/2022-09-15 testing ecg board esp/2022-09-15_16-13-00_test_ecgBoard_esp_suctionCups.csv';

data = readtable(filepath);
t = data.t;
ecg = data.ecg;
lod = data.lod;

t_s = (t-min(t));

% start_index = find(t_s > 45, 1, 'first');
% end_index = find(t_s > 55, 1, 'first');
% t_s = t_s(start_index:end_index);
% ecg = ecg(start_index:end_index);

Fs = length(t_s)/(max(t_s) - min(t_s));
% ecg_filtered = bandstop(ecg, [50, 70], Fs);
ecg_filtered = bandpass(ecg, [3, 30], Fs);

figure(1);
clf;
s1 = subplot(4,1,1);
myplot(t_s, ecg, 'maximize', false);
title('ECG Reading Using Pi: Unfiltered');
ylabel('ADC Reading [0 - 8e6]');
s2 = subplot(4,1,2);
myplot(t_s, ecg_filtered, 'maximize', false);
title('ECG Reading Using Pi: Bandpass Filtered [3, 30] Hz');
s3 = subplot(4,1,3);
myplot(t_s, lod, 'maximize', false);
title('Leads-Off Detection');
linkaxes([s1 s2 s3], 'x');
xlim([min(t_s), max(t_s)]);
% xlabel('Time [s]');


fprintf('\n');
fprintf('\n%d samples', length(t_s));
fprintf('\n%0.2f s', (max(t_s) - min(t_s)));
fprintf('\n%0.2f Hz', length(t_s)/(max(t_s) - min(t_s)));
fprintf('\n');

%%
figure(2); clf;
findpeaks(ecg_filtered, 'annotate', 'extents');
[pks, loc, w, p] = findpeaks(ecg_filtered, 'annotate', 'extents');
figure(3);
histogram(p);

%%
[pks, loc, w, p] = findpeaks(ecg_filtered, 'MinPeakProminence', 5e6);
beats_s = t_s(loc);
beats_diff_s = diff(beats_s);
bpm = 60./beats_diff_s;
lod_smooth = movmean(lod, round(Fs*[0.1 0.1]));
bpm(logical(lod(loc(2:end)))) = nan;
bpm_s = beats_s(2:end);
figure(1);
s4 = subplot(4,1,4);
myplot(bpm_s, bpm, 'maximize', false);
title('Beat-to-Beat Heart Rate');
ylabel('BPM');
ylim([50 100]);
linkaxes([s1 s2 s3 s4], 'x');
xlabel('Time [s]');



