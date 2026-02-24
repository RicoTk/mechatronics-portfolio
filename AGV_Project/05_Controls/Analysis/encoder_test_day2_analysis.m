filename = "encoder_rpm_day2_manual.csv";
T = readtable(filename);

t = T.t_s - T.t_s(1);  % normalize time
rpmRaw = T.rpm_raw;
rpmFilt = T.rpm_filt;

figure;
plot(t, rpmRaw);
hold on;
plot(t, rpmFilt);
hold off;

xlabel("Time (s)");
ylabel("RPM");
legend("rpm raw", "rpm filtered");
title("Encoder RPM Measurement (Manual Rotation)");
grid on;