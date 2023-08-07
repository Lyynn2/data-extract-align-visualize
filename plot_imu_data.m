
% imu_data_filepath = 'P:/MIT/Lab/Whales/ECG/data/2023-06-23 testing imu/test 01 allChannels 50Hz/data_imu.csv';
% imu_data_filepath = 'P:/MIT/Lab/Whales/ECG/data/2023-06-23 testing imu/test 02 allChannels 50Hz/data_imu.csv';
% imu_data_filepath = 'P:/MIT/Lab/Whales/ECG/data/2023-06-23 testing imu/test 03 allChannels 50Hz stationary/data_imu.csv';
% imu_data_filepath = 'P:/MIT/Lab/Whales/ECG/data/2023-06-23 testing imu/test 04 allChannels 50Hz stationary/data_imu.csv';
% imu_data_filepath = 'P:/MIT/Lab/Whales/ECG/data/2023-06-23 testing imu/test 05 allChannels 5Hz stationary/data_imu.csv';
% imu_data_filepath = 'P:/MIT/Lab/Whales/ECG/data/2023-06-23 testing imu/test 06 allChannels 5Hz slowRotations/data_imu.csv';
% imu_data_filepath = 'P:/MIT/Lab/Whales/ECG/data/2023-06-23 testing imu/test 08 onlyAccel 5Hz slowMoving/data_imu.csv';
% imu_data_filepath = 'P:/MIT/Lab/Whales/ECG/data/2023-06-23 testing imu/test 10 onlyAccel 5Hz slowMoving/data_imu.csv';
% imu_data_filepath = 'P:/MIT/Lab/Whales/ECG/data/2023-06-23 testing imu/test 11 allChannels 50Hz sometimesMoving/data_imu.csv';
% imu_data_filepath = 'P:/MIT/Lab/Whales/ECG/data/2023-06-23 testing imu/test 12 allChannels 50Hz mostlyStationary/data_imu.csv';
% imu_data_filepath = 'P:/MIT/Lab/Whales/ECG/data/2023-06-23 testing imu/test 13 allChannels 50Hz mostlyStationary/data_imu.csv';
% imu_data_filepath = 'P:/MIT/Lab/Whales/ECG/data/2023-06-23 testing imu/test 14 allChannels 50Hz perpendiculars/data_imu.csv';
% imu_data_filepath = 'P:/MIT/Lab/Whales/ECG/data/2023-06-23 testing imu/test 15 allChannels 50Hz/data_imu.csv';
% imu_data_filepath = 'P:/MIT/Lab/Whales/ECG/data/2023-06-29 testing imu gopros/test 00 imu file size limit 1mb/';
imu_data_filepath = 'P:/MIT/Lab/Whales/ECG/data/2023-06-29 testing imu gopros/test 01 imu longer someOrientationsThreeTaps/';
if isfile(imu_data_filepath)
    imu_data = readtable(imu_data_filepath);
    imu_data = imu_data(10:end, :);
    fid = fopen(imu_data_filepath);
    fseek(fid, 0, 'eof');
    imu_data_filesize_bytes = ftell(fid);
    fclose(fid);
else
    imu_data_filesize_bytes = 0;
    imu_data = [];
    imu_data_dir = imu_data_filepath;
    imu_data_files = dir(fullfile(imu_data_dir, 'data_imu_*.csv'));
    for file_index = 1:length(imu_data_files)
        imu_data_filepath = fullfile(imu_data_files(file_index).folder, imu_data_files(file_index).name)
        if isempty(imu_data)
            imu_data = readtable(imu_data_filepath);
        else
            imu_data = [imu_data; readtable(imu_data_filepath)];
        end
        size(imu_data)
        fid = fopen(imu_data_filepath);
        fseek(fid, 0, 'eof');
        imu_data_filesize_bytes = imu_data_filesize_bytes + ftell(fid);
        fclose(fid);
    end
end

fprintf('\n');


%%
t = table2array(imu_data(:, 1));
t = t/1e6;
t = (t - min(t));
fprintf('\nDuration: %0.2f seconds (%0.2f minutes) (%0.2f hours) (%0.2f days)', max(t)-min(t), (max(t)-min(t))/60, (max(t)-min(t))/3600, (max(t)-min(t))/3600/24);
fprintf('\nFile size rate: %0.2f MB/hour (%0.2f MB/day)', imu_data_filesize_bytes/1024/1024/((max(t)-min(t))/3600), imu_data_filesize_bytes/1024/1024/((max(t)-min(t))/3600/24));
fprintf('\nAll-sensor message rate: %0.2f Hz (max %6.2f | min %6.2f)', (length(t)-1)/(max(t)-min(t)), 1/min(diff(t)), 1/max(diff(t)));

delay_us = table2array(imu_data(:, 4));
t_delay_us = t(~isnan(delay_us));
delay_us = delay_us(~isnan(delay_us));

quat = table2array(imu_data(:, 5:9));
to_keep = ~(any(isnan(quat),2));
t_quat = t(to_keep);
quat = quat(to_keep, :);
quat_accuracy = quat(:,5) * 2^-12; % accuracy in radians
quat = quat(:,1:4) * 2^-14;
fprintf('\nQuat rate : %6.2f Hz (max %6.2f | min %6.2f)', (size(quat, 1)-1)/(max(t_quat)-min(t_quat)), 1/min(diff(t_quat)), 1/max(diff(t_quat)));

accel = table2array(imu_data(:, 10:13));
to_keep = ~(any(isnan(accel),2));
t_accel = t(to_keep);
accel = accel(to_keep, :);
accel_accuracy = accel(:,4);
accel = accel(:,1:3) * 2^-8; % m/s^2
fprintf('\nAccel rate: %6.2f Hz (max %6.2f | min %6.2f)', (size(accel, 1)-1)/(max(t_accel)-min(t_accel)), 1/min(diff(t_accel)), 1/max(diff(t_accel)));

gyro = table2array(imu_data(:, 14:17));
to_keep = ~(any(isnan(gyro),2));
t_gyro = t(to_keep);
gyro = gyro(to_keep, :);
gyro_accuracy = gyro(:,4);
gyro = gyro(:,1:3) * 2^-9; % rad/s
fprintf('\nGyro rate : %6.2f Hz (max %6.2f | min %6.2f)', (size(gyro, 1)-1)/(max(t_gyro)-min(t_gyro)), 1/min(diff(t_gyro)), 1/max(diff(t_gyro)));

mag = table2array(imu_data(:, 18:21));
to_keep = ~(any(isnan(mag),2));
t_mag = t(to_keep);
mag = mag(to_keep, :);
mag_accuracy = mag(:, 4);
mag = mag(:,1:3) * 2^-4; % micro tesla
fprintf('\nMag rate  : %6.2f Hz (max %6.2f | min %6.2f)', (size(mag, 1)-1)/(max(t_mag)-min(t_mag)), 1/min(diff(t_mag)), 1/max(diff(t_mag)));

fprintf('\n');
fprintf('\n');

%%
% figure(1); clf;
% myplot(t, delay_us/1000);
% ylabel('Sensor Delay [ms]');
% xlabel('Time Since Start [s]');
figure(1); clf;
s = [];
s(end+1) = subplot(4, 1, 1);
% myplot(t_quat, quat); title('Quaternion');
myplot(t_quat, unwrap(quat2eul([quat(:,4) quat(:,1:3)]))); title('Euler Angles'); %ylim([-4 4]); 
s(end+1) = subplot(4, 1, 2);
myplot(t_accel, accel); title('Acceleration'); ylabel('m/s/s');
s(end+1) = subplot(4, 1, 3);
myplot(t_gyro, gyro); title('Angular Velocity'); ylabel('rad/s');
s(end+1) = subplot(4, 1, 4);
myplot(t_mag, mag); title('Magnetic Field'); ylabel('uT');
xlabel('Time Since Start [s]');
linkaxes(s, 'x');

%%
figure(2); clf;
s = [];
s(end+1) = subplot(4, 1, 1);
myplot(t_quat(2:end), 1./diff(t_quat)); title('Quaternion Sampling Rate'); ylabel('Hz'); ylim([0 200]);
s(end+1) = subplot(4, 1, 2);
myplot(t_accel(2:end), 1./diff(t_accel)); title('Acceleration Sampling Rate'); ylabel('Hz'); ylim([0 200]);
s(end+1) = subplot(4, 1, 3);
myplot(t_gyro(2:end), 1./diff(t_gyro)); title('Angular Velocity Sampling Rate'); ylabel('Hz'); ylim([0 200]);
s(end+1) = subplot(4, 1, 4);
myplot(t_mag(2:end), 1./diff(t_mag)); title('Magnetic Field Sampling Rate'); ylabel('Hz'); ylim([0 200]);
xlabel('Time Since Start [s]');
linkaxes(s, 'x');
%%
figure(3); clf;
s = [];
s(end+1) = subplot(4, 1, 1);
myplot(t_quat, quat_accuracy); title('Quaternion Accuracy'); ylabel('rad');
% myplot(t_quat, quat2eul([quat(:,4) quat(:,1:3)])); title('Euler Angles');
s(end+1) = subplot(4, 1, 2);
myplot(t_accel, accel_accuracy); title('Acceleration Accuracy'); ylabel('0-3 [0 bad]'); ylim([0 3]);
s(end+1) = subplot(4, 1, 3);
myplot(t_gyro, gyro_accuracy); title('Angular Velocity Accuracy'); ylabel('0-3 [0 bad]'); ylim([0 3]);
s(end+1) = subplot(4, 1, 4);
myplot(t_mag, mag_accuracy); title('Magnetic Field Accuracy'); ylabel('0-3 [0 bad]'); ylim([0 3]);
xlabel('Time Since Start [s]');
linkaxes(s, 'x');




