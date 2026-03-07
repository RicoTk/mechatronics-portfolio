filename = "step_test_data.csv";
T = readtable(filename);


len_cols = height(T);
t_curr = T.t_ms(1);
t_end = T.t_ms(end);
t_date = [];
i = 1;

%while loop going through t_ms column and transforming milliseconds to
%datetime
for i = 1:279
    t_new = datetime(T.t_ms(i), 'ConvertFrom', 'epochtime','Epoch','Jan 1, 2000', 'TicksPerSecond', 1000);
    t_new.Format = 'yyyy-MM-dd HH:mm:ss.SSS';
    t_date = [t_date; t_new]; %appending values dynamically to array in form of column
    i = i + 1;
end

%checking size of all major variables for plots
a = size(t_date);
b = size(T.speed_raw);
c = size(T.curr_A);

%Creating new table with datetime for intervals
Step_Test_Table = timetable(t_date, T.speed_raw, T.curr_A);

% Select data intervals (0 -> 2000 -> 6000 -> 10000 -> etc...
startTime = datetime(2000,1,1,00,00,00,22000);
endTime = datetime(2000,1,1,00,00,00,26000);
RPM_0_4s_going_down = Step_Test_Table(timerange(startTime, endTime), :);

