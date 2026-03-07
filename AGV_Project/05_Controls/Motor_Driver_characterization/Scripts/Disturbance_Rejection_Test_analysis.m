filename = "Disturbance_Rejection_data.csv";
T = readtable(filename);

t = T.t_ms - T.t_ms(1) % normalize time
speedRaw = T.speed_raw;
currentA = T.curr_A;

% Plot overall step test data
figure;
yyaxis left;
plot(T.t_ms, T.speed_raw, 'b', 'DisplayName', 'Full Data'); % Plot all data in black
hold on; % Hold the current plot to add more lines
yyaxis right;
plot(T.t_ms, T.curr_A, 'r', 'DisplayName', 'Full Data');
hold off;

title('Disturbance Rejection - Time vs Actual Speed and Current')
xlabel('Time (ms)')
yyaxis left
ylabel('Speed (RPM)')
yyaxis right
ylabel('Current (A)')


speed_intervals = [0, 2000, 10000, 14000, 22000, 26000];
step_intervals_titles = ["Disturbance Rejection - Time vs Actual Speed and Current (0 RPM - 2 seconds)",...
                         "Disturbance Rejection - Time vs Actual Speed and Current (1500 RPM - 8 seconds)",...
                         "Disturbance Rejection - Time vs Actual Speed and Current (0 RPM - 4 seconds)"...
                         "Disturbance Rejection - Time vs Actual Speed and Current (2500 RPM - 8 seconds)",...
                         "Disturbance Rejection - Time vs Actual Speed and Current(0 RPM - 4 seconds)"];
                         

for i = 1:5

    xmin = speed_intervals(i);
    xmax = speed_intervals(i + 1);
    
    % 3. Use logical indexing to select data within the interval
    %    McIdx is a logical array where 'true' indicates data within the range
    McIdx = (T.t_ms >= xmin) & (T.t_ms <= xmax);
    
    % 4. Plot the data
    figure;
    yyaxis left;
    plot(T.t_ms(McIdx), T.speed_raw(McIdx), 'b', 'DisplayName', 'Full Data'); % Plot all data in black
    hold on; % Hold the current plot to add more lines
    yyaxis right;
    plot(T.t_ms(McIdx), T.curr_A(McIdx), 'r', 'DisplayName', 'Full Data');
    hold off;
    
    title(step_intervals_titles(i))
    xlabel('Time (ms)')
    yyaxis left
    ylabel('Speed (RPM)')
    yyaxis right
    ylabel('Current (A)')

end

