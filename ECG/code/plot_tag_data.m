
%%
% data_dir = 'P:/MIT/Lab/Whales/ECG/data/2023-07-04 - 01 before deployment/test 03 tagv2-2_1 2ecgCycles';
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-04 testing ecg\test 00 v2-2_2 separateHandsThumbGnd';
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-04 testing ecg\test 01 v2-2_2 separateHandsLT-RM-RTgnd_paste';
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-04 testing ecg\test 02 v2-2_1 separateHandsLT-RM-RTgnd_noPaste';
% data_dir = 'P:\MIT\Lab\Whales\ECG\data\2023-07-04 testing ecg\test 03 v2-2_1 separateHandsLT-RM-RTgnd_noPaste';
data_dir = 'P:\MIT\Lab\Whales\ECG\data\_deployments\2023-07-06 deployed tag v2-2_1 with ECG';

ecg_filter_passband = [2, 100];
plot_ecg_figure = true;

plot_pressure_data = true;
plot_ecg_depth_motion = true;

% rtc_to_utc_offset = 1688555972492670.00/1e6 - 2216066;
diveSegment_start_rtc = 2235210;
diveSegment_end_rtc = 2240830;

%% Load data

% ECG
ecg_data_filesize_bytes = 0;
ecg_data = [];
ecg_data_dir = data_dir;
ecg_data_files = dir(fullfile(ecg_data_dir, 'data_ecg_*.csv'));
for file_index = 1:length(ecg_data_files)
    data_filepath = fullfile(ecg_data_files(file_index).folder, ecg_data_files(file_index).name);
    if isempty(ecg_data)
        ecg_data = readtable(data_filepath);
    else
        ecg_data = [ecg_data; readtable(data_filepath)];
    end
    fid = fopen(data_filepath);
    fseek(fid, 0, 'eof');
    ecg_data_filesize_bytes = ecg_data_filesize_bytes + ftell(fid);
    fclose(fid);
end
% ecg_data = ecg_data(1:round(size(ecg_data, 1)*0.9), :);

% IMU
imu_data_filesize_bytes = 0;
imu_data = [];
imu_data_files = dir(fullfile(data_dir, 'data_imu_*.csv'));
for file_index = 1:length(imu_data_files)
    imu_data_filepath = fullfile(imu_data_files(file_index).folder, imu_data_files(file_index).name);
    if isempty(imu_data)
        imu_data = readtable(imu_data_filepath);
    else
        imu_data = [imu_data; readtable(imu_data_filepath)];
    end
    fid = fopen(imu_data_filepath);
    fseek(fid, 0, 'eof');
    imu_data_filesize_bytes = imu_data_filesize_bytes + ftell(fid);
    fclose(fid);
end
% imu_data = imu_data(1:round(size(imu_data, 1)*0.9), :);

% Pressure/temperature
pressureTemperature_data_filesize_bytes = 0;
pressureTemperature_data = [];
pressureTemperature_data_files = dir(fullfile(data_dir, 'data_pressure_temperature*.csv'));
for file_index = 1:length(pressureTemperature_data_files)
    pressureTemperature_data_filepath = fullfile(pressureTemperature_data_files(file_index).folder, pressureTemperature_data_files(file_index).name);
    if isempty(pressureTemperature_data)
        pressureTemperature_data = readtable(pressureTemperature_data_filepath);
    else
        pressureTemperature_data = [pressureTemperature_data; readtable(pressureTemperature_data_filepath)];
    end
    fid = fopen(pressureTemperature_data_filepath);
    fseek(fid, 0, 'eof');
    pressureTemperature_data_filesize_bytes = pressureTemperature_data_filesize_bytes + ftell(fid);
    fclose(fid);
end
% pressureTemperature_data = pressureTemperature_data(1:round(size(pressureTemperature_data, 1)*0.9), :);

% Light
light_data_filesize_bytes = 0;
light_data = [];
light_data_files = dir(fullfile(data_dir, 'data_light*.csv'));
for file_index = 1:length(light_data_files)
    light_data_filepath = fullfile(light_data_files(file_index).folder, light_data_files(file_index).name);
    if isempty(light_data)
        light_data = readtable(light_data_filepath);
    else
        light_data = [light_data; readtable(light_data_filepath)];
    end
    fid = fopen(light_data_filepath);
    fseek(fid, 0, 'eof');
    light_data_filesize_bytes = light_data_filesize_bytes + ftell(fid);
    fclose(fid);
end
% light_data = light_data(1:round(size(light_data, 1)*0.9), :);

%% Process ECG data
% Extract original time
ecg_rtc = ecg_data.RTCCount;
diveSegment_start_index_ecg = find(ecg_rtc >= diveSegment_start_rtc, 1, 'first');
diveSegment_end_index_ecg = find(ecg_rtc <= diveSegment_end_rtc, 1, 'last');
ecg_data = ecg_data(diveSegment_start_index_ecg:diveSegment_end_index_ecg, :);

ecg_t_raw = table2array(ecg_data(:, 1));
ecg_rtc = ecg_data.RTCCount;
ecg_t = ecg_data.Timestamp_us_/1e6;
ecg_dt = diff(ecg_t);

start_time_s = ecg_t(1);
ecg_t = ecg_t - start_time_s;

% ecg_t = fix_tag_time_vector(ecg_t_raw/1e6, ecg_rtc, 1);
% figure; subplot(2,1,1);
% myplot(ecg_t_raw);
% subplot(2,1,2);
% myplot(ecg_t);
%
% ecg_dt = diff(ecg_t);
% 
% % Fix the final jump
% jump_start_index = find(ecg_dt < -100, 1, 'first')+1;
% ecg_t(jump_start_index:end) = ecg_t(jump_start_index:end) - ecg_t(jump_start_index);
% ecg_t(jump_start_index:end) = ecg_t(jump_start_index:end) + (rtc_to_utc_offset + ecg_rtc(jump_start_index))*1e6;
% % Get time since start in seconds
% ecg_t = ecg_t - min(ecg_t);
% ecg_t = ecg_t/1e6;
% ecg_dt = diff(ecg_t);

ecg = ecg_data.ECG;
ecg_leadson_p = 1-ecg_data.Leads_Off_P;
ecg_leadson_n = 1-ecg_data.Leads_Off_N;

% Ignore the last index for now
% ecg_t = ecg_t(1:end-1);
% ecg = ecg(1:end-1);
% ecg_leadson_p = ecg_leadson_p(1:end-1);
% ecg_leadson_n = ecg_leadson_n(1:end-1);
% ecg_dt = diff(ecg_t);

% if any(abs(ecg_dt) > 100)
%     first_index = find(abs(ecg_dt) > 100, 1, 'last')+1;
%     ecg_t = ecg_t(first_index:end);
%     ecg = ecg(first_index:end);
%     ecg_leadson_p = ecg_leadson_p(first_index:end);
%     ecg_leadson_n = ecg_leadson_n(first_index:end);
%     ecg_dt = diff(ecg_t);
%     fprintf('\n');
%     warning('Starting ECG at index %d to avoid large time jump', first_index);
%     fprintf('\n');
% end

ecg_Fs = (length(ecg_t)-1)/range(ecg_t);
if ~isempty(ecg_filter_passband)
    ecg_filtered = bandpass(ecg, ecg_filter_passband, ecg_Fs);
end
ecg_leadson = ecg_leadson_p & ecg_leadson_n;

%% Process IMU data
imu_rtc = imu_data.RTCCount;
diveSegment_start_index_imu= find(imu_rtc >= diveSegment_start_rtc, 1, 'first');
diveSegment_end_index_imu = find(imu_rtc <= diveSegment_end_rtc, 1, 'last');
imu_data = imu_data(diveSegment_start_index_imu:diveSegment_end_index_imu, :);

imu_t_raw = table2array(imu_data(:, 1));
imu_rtc = imu_data.RTCCount;
imu_t = imu_data.Timestamp_us_/1e6;
imu_t = imu_t - start_time_s;
imu_dt = diff(imu_t);
% imu_t = fix_tag_time_vector(imu_t_raw/1e6, imu_rtc, 1);

% % Extract original time
% imu_t = table2array(imu_data(:, 1));
% imu_dt = diff(imu_t);
% imu_rtc = imu_data.RTCCount;
% % Fix the final jump
% jump_start_index = find(imu_dt < -100, 1, 'first')+1;
% imu_t(jump_start_index:end) = imu_t(jump_start_index:end) - imu_t(jump_start_index);
% imu_t(jump_start_index:end) = imu_t(jump_start_index:end) + (rtc_to_utc_offset + imu_rtc(jump_start_index))*1e6;
% % Get time since start in seconds
% imu_t = imu_t - min(imu_t);
% imu_t = imu_t/1e6;
% imu_dt = diff(imu_t);

% if any(abs(imu_dt) > 100)
%     first_index = find(abs(imu_dt) > 100, 1, 'last')+1;
%     imu_t = imu_t(first_index:end);
%     imu_data = imu_data(first_index:end);
%     imu_dt = diff(imu_t);
%     fprintf('\n');
%     warning('Starting IMU at index %d to avoid large time jump', first_index);
%     fprintf('\n');
% end
imu_Fs = (length(imu_t)-1)/range(imu_t);

imu_delay_us = table2array(imu_data(:, 4));
imu_t_delay_us = imu_t(~isnan(imu_delay_us));
imu_delay_us = imu_delay_us(~isnan(imu_delay_us));

imu_quat = table2array(imu_data(:, 5:9));
imu_to_keep = ~(any(isnan(imu_quat),2));
imu_t_quat = imu_t(imu_to_keep);
imu_quat = imu_quat(imu_to_keep, :);
imu_quat_accuracy = imu_quat(:,5) * 2^-12; % accuracy in radians
imu_quat = imu_quat(:,1:4) * 2^-14;
imu_euler_rad = unwrap(quat2eul([imu_quat(:,4) imu_quat(:,1:3)]));

imu_accel_m_ss = table2array(imu_data(:, 10:13));
imu_to_keep = ~(any(isnan(imu_accel_m_ss),2));
imu_t_accel = imu_t(imu_to_keep);
imu_accel_m_ss = imu_accel_m_ss(imu_to_keep, :);
imu_accel_accuracy = imu_accel_m_ss(:,4);
imu_accel_m_ss = imu_accel_m_ss(:,1:3) * 2^-8; % m/s^2
imu_accel_norm_m_ss = vecnorm(imu_accel_m_ss')';

imu_gyro_rad_s = table2array(imu_data(:, 14:17));
imu_to_keep = ~(any(isnan(imu_gyro_rad_s),2));
imu_t_gyro = imu_t(imu_to_keep);
imu_gyro_rad_s = imu_gyro_rad_s(imu_to_keep, :);
imu_gyro_accuracy = imu_gyro_rad_s(:,4);
imu_gyro_rad_s = imu_gyro_rad_s(:,1:3) * 2^-9; % rad/s

imu_mag_uT = table2array(imu_data(:, 18:21));
imu_to_keep = ~(any(isnan(imu_mag_uT),2));
imu_t_mag = imu_t(imu_to_keep);
imu_mag_uT = imu_mag_uT(imu_to_keep, :);
imu_mag_accuracy = imu_mag_uT(:, 4);
imu_mag_uT = imu_mag_uT(:,1:3) * 2^-4; % micro tesla

%% Process Pressure/Temperature data
pressure_rtc = pressureTemperature_data.RTCCount;
diveSegment_start_index_pressure = find(pressure_rtc >= diveSegment_start_rtc, 1, 'first');
diveSegment_end_index_pressure = find(pressure_rtc <= diveSegment_end_rtc, 1, 'last');
pressureTemperature_data = pressureTemperature_data(diveSegment_start_index_pressure:diveSegment_end_index_pressure, :);

pressure_t_raw = table2array(pressureTemperature_data(:, 1));
pressure_t = pressureTemperature_data.Timestamp_us_/1e6;
pressure_t = pressure_t - start_time_s;
pressure_rtc = pressureTemperature_data.RTCCount;
% pressure_t = fix_tag_time_vector(pressure_t_raw/1e6, pressure_rtc, 1);

% % Extract original time
% pressure_t = table2array(pressureTemperature_data(:, 1));
% pressure_dt = diff(pressure_t);
% pressure_rtc = pressureTemperature_data.RTCCount;
% % Fix the final jump
% jump_start_index = find(pressure_dt < -100, 1, 'first')+1;
% pressure_t(jump_start_index:end) = pressure_t(jump_start_index:end) - pressure_t(jump_start_index);
% pressure_t(jump_start_index:end) = pressure_t(jump_start_index:end) + (rtc_to_utc_offset + pressure_rtc(jump_start_index))*1e6;
% % Get time since start in seconds
% pressure_t = pressure_t - min(pressure_t);
% pressure_t = pressure_t/1e6;
% pressure_dt = diff(pressure_t);

pressure_dt = diff(pressure_t);
temperature_t = pressure_t;
temperature_dt = pressure_dt;

pressure_bar = pressureTemperature_data.Pressure_bar_;
temperature_c = pressureTemperature_data.WaterTemperature_C_;

% See https://journals.ametsoc.org/view/journals/phoc/11/4/1520-0485_1981_011_0573_pcoptd_2_0_co_2.xml
c1 = (5.92+5.25*sin(deg2rad(15.28550833469743))^2)/1e3;
c2 = 2.21/1e6;
depth_m = (1-c1)*(pressure_bar*10) - c2*(pressure_bar*10).^2;

% if any(abs(pressure_dt) > 100)
%     first_index = find(abs(pressure_dt) > 100, 1, 'last')+1;
%     pressure_t = pressure_t(first_index:end);
%     pressure_bar = pressure_bar(first_index:end);
%     temperature_c = temperature_c(first_index:end);
%     pressure_dt = diff(pressure_t);
%     temperature_dt = pressure_dt;
%     fprintf('\n');
%     warning('Starting pressure/temperature at index %d to avoid large time jump', first_index);
%     fprintf('\n');
% end
pressure_Fs = (length(pressure_t)-1)/range(pressure_t);
temperature_Fs = pressure_Fs;

%% Process Light data
light_rtc = light_data.RTCCount;
diveSegment_start_index_light = find(light_rtc >= diveSegment_start_rtc, 1, 'first');
diveSegment_end_index_light = find(light_rtc <= diveSegment_end_rtc, 1, 'last');
light_data = light_data(diveSegment_start_index_light:diveSegment_end_index_light, :);

light_t_raw = table2array(light_data(:, 1));
light_t = light_data.Timestamp_us_/1e6;
light_t = light_t - start_time_s;
light_rtc = light_data.RTCCount;
% light_t = fix_tag_time_vector(light_t_raw/1e6, light_rtc, 1);

% light_t = table2array(light_data(:, 1));
% ecg_t_raw = table2array(ecg_data(:, 1));
% ecg_rtc = ecg_data.RTCCount;
% ecg_t = fix_tag_time_vector(ecg_t_raw/1e6, ecg_rtc, 1);light_t = light_t/1e6;
% light_t = (light_t - min(light_t));
light_dt = diff(light_t);
light_visible = light_data.AmbientLight_Visible;
light_ir = light_data.AmbientLight_IR;

% if any(abs(light_dt) > 100)
%     first_index = find(abs(light_dt) > 100, 1, 'last')+1;
%     light_t = light_t(first_index:end);
%     light_visible = light_visible(first_index:end);
%     light_ir = light_ir(first_index:end);
%     light_dt = diff(light_t);
%     fprintf('\n');
%     warning('Starting light at index %d to avoid large time jump', first_index);
%     fprintf('\n');
% end
light_Fs = (length(light_t)-1)/range(light_t);

%% Print Summaries
fprintf('\n');
fprintf('\n');
fprintf('\n');
fprintf('ECG Summary');
fprintf('\n  Duration: %0.2f seconds (%0.2f minutes) (%0.2f hours) (%0.2f days)', max(ecg_t)-min(ecg_t), (max(ecg_t)-min(ecg_t))/60, (max(ecg_t)-min(ecg_t))/3600, (max(ecg_t)-min(ecg_t))/3600/24);
ecg_filesize_rate_mb_hr = ecg_data_filesize_bytes/1024/1024/((max(ecg_t)-min(ecg_t))/3600);
fprintf('\n  File size: %0.2f MB (%0.2f GB)', ecg_data_filesize_bytes/1024/1024, ecg_data_filesize_bytes/1024/1024/1024);
fprintf('\n  File size rate: %0.2f MB/hour (%0.2f MB/day) (%0.2f GB/day)', ecg_filesize_rate_mb_hr, ecg_filesize_rate_mb_hr*24, ecg_filesize_rate_mb_hr*24/1024);
fprintf('\n  All-sensor message rate: %0.2f Hz (max %6.2f | min %6.2f)', (length(ecg_t)-1)/(max(ecg_t)-min(ecg_t)), 1/min(diff(ecg_t)), 1/max(diff(ecg_t)));

fprintf('\nIMU Summary');
fprintf('\n  Duration: %0.2f seconds (%0.2f minutes) (%0.2f hours) (%0.2f days)', max(imu_t)-min(imu_t), (max(imu_t)-min(imu_t))/60, (max(imu_t)-min(imu_t))/3600, (max(imu_t)-min(imu_t))/3600/24);
imu_filesize_rate_mb_hr = imu_data_filesize_bytes/1024/1024/((max(imu_t)-min(imu_t))/3600);
fprintf('\n  File size: %0.2f MB (%0.2f GB)', imu_data_filesize_bytes/1024/1024, imu_data_filesize_bytes/1024/1024/1024);
fprintf('\n  File size rate: %0.2f MB/hour (%0.2f MB/day) (%0.2f GB/day)', imu_filesize_rate_mb_hr, imu_filesize_rate_mb_hr*24, imu_filesize_rate_mb_hr*24/1024);
fprintf('\n  All-sensor message rate: %0.2f Hz (max %6.2f | min %6.2f)', (length(imu_t)-1)/(max(imu_t)-min(imu_t)), 1/min(diff(imu_t)), 1/max(diff(imu_t)));
fprintf('\n  Quat rate : %6.2f Hz (max %6.2f | min %6.2f)', (size(imu_quat, 1)-1)/(max(imu_t_quat)-min(imu_t_quat)), 1/min(diff(imu_t_quat)), 1/max(diff(imu_t_quat)));
fprintf('\n  Accel rate: %6.2f Hz (max %6.2f | min %6.2f)', (size(imu_accel_m_ss, 1)-1)/(max(imu_t_accel)-min(imu_t_accel)), 1/min(diff(imu_t_accel)), 1/max(diff(imu_t_accel)));
fprintf('\n  Gyro rate : %6.2f Hz (max %6.2f | min %6.2f)', (size(imu_gyro_rad_s, 1)-1)/(max(imu_t_gyro)-min(imu_t_gyro)), 1/min(diff(imu_t_gyro)), 1/max(diff(imu_t_gyro)));
fprintf('\n  Mag rate  : %6.2f Hz (max %6.2f | min %6.2f)', (size(imu_mag_uT, 1)-1)/(max(imu_t_mag)-min(imu_t_mag)), 1/min(diff(imu_t_mag)), 1/max(diff(imu_t_mag)));

fprintf('\nPressure/Temperature Summary');
fprintf('\n  Duration: %0.2f seconds (%0.2f minutes) (%0.2f hours) (%0.2f days)', max(pressure_t)-min(pressure_t), (max(pressure_t)-min(pressure_t))/60, (max(pressure_t)-min(pressure_t))/3600, (max(pressure_t)-min(pressure_t))/3600/24);
pressure_filesize_rate_mb_hr = pressureTemperature_data_filesize_bytes/1024/1024/((max(pressure_t)-min(pressure_t))/3600);
fprintf('\n  File size: %0.2f MB (%0.2f GB)', pressureTemperature_data_filesize_bytes/1024/1024, pressureTemperature_data_filesize_bytes/1024/1024/1024);
fprintf('\n  File size rate: %0.2f MB/hour (%0.2f MB/day) (%0.2f GB/day)', pressure_filesize_rate_mb_hr, pressure_filesize_rate_mb_hr*24, pressure_filesize_rate_mb_hr*24/1024);
fprintf('\n  All-sensor message rate: %0.2f Hz (max %6.2f | min %6.2f)', (length(pressure_t)-1)/(max(pressure_t)-min(pressure_t)), 1/min(diff(pressure_t)), 1/max(diff(pressure_t)));

fprintf('\nLight Summary');
fprintf('\n  Duration: %0.2f seconds (%0.2f minutes) (%0.2f hours) (%0.2f days)', max(light_t)-min(light_t), (max(light_t)-min(light_t))/60, (max(light_t)-min(light_t))/3600, (max(light_t)-min(light_t))/3600/24);
light_filesize_rate_mb_hr = light_data_filesize_bytes/1024/1024/((max(light_t)-min(light_t))/3600);
fprintf('\n  File size: %0.2f MB (%0.2f GB)', light_data_filesize_bytes/1024/1024, light_data_filesize_bytes/1024/1024/1024);
fprintf('\n  File size rate: %0.2f MB/hour (%0.2f MB/day) (%0.2f GB/day)', light_filesize_rate_mb_hr, light_filesize_rate_mb_hr*24, light_filesize_rate_mb_hr*24/1024);
fprintf('\n  All-sensor message rate: %0.2f Hz (max %6.2f | min %6.2f)', (length(light_t)-1)/(max(light_t)-min(light_t)), 1/min(diff(light_t)), 1/max(diff(light_t)));
fprintf('\n');

fprintf('\n');

%% Plot ECG data
if plot_ecg_figure
    figure(1); clf;
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
    xlabel('Time Since Start [seconds]');
    ylim([500 1500]);
    
    linkaxes(subplot_handles, 'x');
    % xlim([150 175]);
end

%% Plot pressure data
if plot_pressure_data
    figure(2); clf;
    subplot_handles = [];
    subplot_handles(end+1) = subplot(2,1,1);
    myplot(pressure_t, -depth_m);
    title('Diving');
    ylabel('Depth [m]');
    subplot_handles(end+1) = subplot(2,1,2);
    myplot((temperature_t-min(temperature_t)), temperature_c);
    title('Water Temperature');
    xlabel('Time Since Start [seconds]');
    ylabel('Temperature [C]');
    linkaxes(subplot_handles, 'x');

    figure(7); clf;
    subplot_handles = [];
    subplot_handles(end+1) = subplot(3,1,1);
    myplot(pressure_t, -depth_m);
    title('Diving');
    ylabel('Depth [m]');
    subplot_handles(end+1) = subplot(3,1,2);
    myplot(temperature_t, temperature_c);
    title('Water Temperature');
    ylabel('Temperature [C]');
    subplot_handles(end+1) = subplot(3,1,3);
    myplot(light_t, light_visible, 'name', 'Visible');
    myplot(light_t, light_ir, 'name', 'IR');
    title('Visible and IR Light');
    xlabel('Time Since Start [seconds]');
    ylabel('Light Reading');
    linkaxes(subplot_handles, 'x');
end


%% Plot combination
if plot_ecg_depth_motion
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
    myplot(ecg_leadson_x, min(ylim)*ones(size(ecg_leadson_x)), 'g-', 'linewidth', 4);
    if ~isempty(ecg_filter_passband)
        title(sprintf('ECG Signal (Filtered [%g, %g] Hz)', ecg_filter_passband(1), ecg_filter_passband(2)));
    else
        title('ECG Signal (Unfiltered)');
    end
    ylabel('ADC Value');

    subplot_handles(end+1) = subplot(3,1,2);
    myplot(pressure_t, -depth_m);
    title('Diving');
    ylabel('Depth [m]');

    subplot_handles(end+1) = subplot(3,1,3);
    myplot(imu_t_accel, imu_accel_norm_m_ss);
    title('Motion');
    ylabel('Acceleration [m/s/s]');
    ylim([5 20]);
    
    xlabel('Time Since Start [seconds]');

    linkaxes(subplot_handles, 'x');
end



