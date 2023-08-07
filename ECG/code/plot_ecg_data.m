
%%
% data_dir = 'P:/MIT/Lab/Whales/ECG/data/2023-07-04 - 01 before deployment/test 03 tagv2-2_1 2ecgCycles';
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-04 testing ecg\test 00 v2-2_2 separateHandsThumbGnd';
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-04 testing ecg\test 01 v2-2_2 separateHandsLT-RM-RTgnd_paste';
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-04 testing ecg\test 02 v2-2_1 separateHandsLT-RM-RTgnd_noPaste';
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-04 testing ecg\test 03 v2-2_1 separateHandsLT-RM-RTgnd_noPaste';
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-05 testing ecg\test 00 v2-2_2 gain44 separateHandsLT-RM-RTgnd_noPaste';
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-05 testing ecg\test 01 v2-2_2 gain44 separateHandsLT-RM-RTgnd_paste'; % No HR? 
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-05 testing ecg\test 02 v2-2_2 gain44 rescrew separateHandsLT-RM-RTgnd_paste'; % LOP 
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-05 testing ecg\test 03 v2-2_2 gain44 barbs separateHandsLT-RM-RTgnd'; % LOP 
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-05 testing ecg\test 04 v2-2_2 gain44 barbs separateHandsLT-RM-RTgnd'; % LOP 
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-05 testing ecg\test 05 v2-2_3 gain87 barbs separateHandsLT-RM-RTgnd'; % 
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-05 testing ecg\test 06 v2-2_3 gain87 separateHandsLT-RM-RTgnd_noPaste';
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-06 testing ecg\test 00 v2-2_2 newCups gain44 separateHandsLT-RM-RTgnd';
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-06 testing ecg\test 01 v2-2_2 sameCups gain44 separateHandsLT-RM-RTgnd';
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-06 testing ecg\test 02 v2-2_3 olderCups gain87 separateHandsLT-RM-RTgnd';
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-06 testing ecg\test 03 v2-2_3 newGreenCups gain87 separateHandsLT-RM-RTgnd';
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-06 testing ecg\test 04 v2-2_3 newGreenCups gain87 separateHandsLT-RM-RTgnd gpioExpander';
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-06 testing ecg\test 05 v2-2_3 newGreenCups gain87 separateHandsLT-RM-RTgnd direct';
data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-07 testing ecg\test 00 v2-2_4 gain44 separateHandsLT-RM-RTgnd_noPaste'; % LON, signal but no HR
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-07 testing ecg\test 01 v2-2_2 gain44 separateHandsLT-RM-RTgnd_noPaste';
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-07 testing ecg\test 02 v2-2_2 gain44 separateHandsLF-RP-RFgnd_noPaste'; % LOP

ecg_filter_passband = [10, 40]; % empty to not filter
plot_fft = false;

%% Load ECG data
ecg_data_filesize_bytes = 0;
ecg_data = [];
ecg_data_dir = data_dir;
ecg_data_files = dir(fullfile(ecg_data_dir, 'data_ecg_*.csv'));
for file_index = 1:length(ecg_data_files)
    data_dir = fullfile(ecg_data_files(file_index).folder, ecg_data_files(file_index).name);
    if isempty(ecg_data)
        ecg_data = readtable(data_dir);
    else
        ecg_data = [ecg_data; readtable(data_dir)];
    end
    fid = fopen(data_dir);
    fseek(fid, 0, 'eof');
    ecg_data_filesize_bytes = ecg_data_filesize_bytes + ftell(fid);
    fclose(fid);
end

ecg_t = table2array(ecg_data(:, 1));
ecg_t = ecg_t/1e6;
ecg_t = (ecg_t - min(ecg_t));
ecg_dt = diff(ecg_t);
ecg = ecg_data.ECG;
ecg_leadson_p = 1-ecg_data.Leads_Off_P;
ecg_leadson_n = 1-ecg_data.Leads_Off_N;

if any(abs(ecg_dt) > 100)
    first_index = find(abs(ecg_dt) > 100, 1, 'last')+1;
    ecg_t = ecg_t(first_index:end);
    ecg = ecg(first_index:end);
    ecg_leadson_p = ecg_leadson_p(first_index:end);
    ecg_leadson_n = ecg_leadson_n(first_index:end);
    fprintf('\n');
    warning('Starting at index %d to avoid large time jump', first_index);
    fprintf('\n');
end

fprintf('\n');
fprintf('\nDuration: %0.2f seconds (%0.2f minutes) (%0.2f hours) (%0.2f days)', max(ecg_t)-min(ecg_t), (max(ecg_t)-min(ecg_t))/60, (max(ecg_t)-min(ecg_t))/3600, (max(ecg_t)-min(ecg_t))/3600/24);
ecg_filesize_rate_mb_hr = ecg_data_filesize_bytes/1024/1024/((max(ecg_t)-min(ecg_t))/3600);
fprintf('\nFile size: %0.2f MB (%0.2f GB)', ecg_data_filesize_bytes/1024/1024, ecg_data_filesize_bytes/1024/1024/1024);
fprintf('\nFile size rate: %0.2f MB/hour (%0.2f MB/day) (%0.2f GB/day)', ecg_filesize_rate_mb_hr, ecg_filesize_rate_mb_hr*24, ecg_filesize_rate_mb_hr*24/1024);
fprintf('\nAll-sensor message rate: %0.2f Hz (max %6.2f | min %6.2f)', (length(ecg_t)-1)/(max(ecg_t)-min(ecg_t)), 1/min(diff(ecg_t)), 1/max(diff(ecg_t)));
fprintf('\n');

%% Process
Fs = (length(ecg_t)-1)/range(ecg_t);
if ~isempty(ecg_filter_passband)
    ecg_filtered = bandpass(ecg, ecg_filter_passband, Fs);
end
ecg_leadson = ecg_leadson_p & ecg_leadson_n;

%% Plot ECG data
figure(3); clf;
subplot_handles = [];
subplot_handles(end+1) = subplot(3,1,1);
if ~isempty(ecg_filter_passband)
    myplot(ecg_t, ecg_filtered);
else
    myplot(ecg_t, ecg);
end
ecg_leadson_rising = get_rising_edges(ecg_leadson, @(x) x == 1);
ecg_leadson_falling = get_rising_edges(ecg_leadson, @(x) x == 0);
ecg_leadson_x = ecg_t([ecg_leadson_rising ecg_leadson_falling]');
% ecg_leadsoff_rising = get_rising_edges(~ecg_leadson, @(x) x == 1);
% ecg_leadsoff_falling = get_rising_edges(~ecg_leadson, @(x) x == 0);
% ecg_leadsoff_x = ecg_t([ecg_leadsoff_rising ecg_leadsoff_falling]');
myplot(ecg_leadson_x, min(ylim)*ones(size(ecg_leadson_x)), 'g-', 'linewidth', 4);
% myplot(ecg_leadsoff_x, -1.5e6*ones(size(ecg_leadsoff_x)), 'r-');

if ~isempty(ecg_filter_passband)
    title(sprintf('ECG Signal (Filtered [%g, %g] Hz)', ecg_filter_passband(1), ecg_filter_passband(2)));
else
    title('ECG Signal (Unfiltered)');
end
ylabel('ADC Value');
% ylim([-2e6 max(ylim)]);

subplot_handles(end+1) = subplot(3,1,2);
myplot(ecg_t, ecg_leadson_p, 'name', 'Positive');
myplot(ecg_t, ecg_leadson_n+0.02, 'm', 'name', 'Negative');
title('Leads-On Detection');

subplot_handles(end+1) = subplot(3,1,3);
myplot(ecg_t(2:end), 1./ecg_dt);
title('Instantaneous Sampling Rate');
ylabel('Sampling Rate [Hz]');
xlabel('Time [s]');
% ylim([500 1500]);

linkaxes(subplot_handles, 'x');
% xlim([165 185]);

%% FFT
if plot_fft
    L = length(ecg_t);
    Y = fft(ecg-mean(ecg));
    P2 = abs(Y/L);
    P1 = P2(1:L/2+1);
    P1(2:end-1) = 2*P1(2:end-1);
    f = Fs*(0:(L/2))/L;
    figure(2); clf;
    plot(f,P1) 
    title("Single-Sided Amplitude Spectrum of X(t)")
    xlabel("f (Hz)")
    ylabel("|P1(f)|")
end





