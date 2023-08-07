
function t_fixed_s = fix_tag_time_vector(t_s, rtc, correct_timestamp_index)
    rtc_to_utc_offset_s = (t_s(correct_timestamp_index) - rtc(correct_timestamp_index));
    dt_s = [0; diff(t_s)];
    t_fixed_s = t_s;
    indexes_to_use_rtc = find(abs(dt_s) > 60);
    for i = 1:length(indexes_to_use_rtc)
        index_to_use_rtc = indexes_to_use_rtc(i)
        t_fixed_s(index_to_use_rtc) = rtc(index_to_use_rtc) + rtc_to_utc_offset_s;
        if index_to_use_rtc == indexes_to_use_rtc(end)
            last_index = length(t_fixed_s)
        else
            last_index = indexes_to_use_rtc(i+1)
        end
        t_fixed_s(index_to_use_rtc:last_index) = t_fixed_s(index_to_use_rtc) + cumsum(dt_s(index_to_use_rtc:last_index));
    end        
end