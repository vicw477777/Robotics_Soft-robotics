% Q4ii

model_name = 'HomeworkSimscape_MatlabR2023a'; 

k_values = [1, 10, 100];     
all_sim_data = cell(1, 3);   

for i = 1:length(k_values)
    k_spring = k_values(i);
    fprintf('Running simulation %d/3 for k = %d N/m... ', i, k_spring);
    
    try
        out = sim(model_name);
        
        data_snapshot = struct(); 
        data_snapshot.cube1 = out.cube1;
        data_snapshot.cube2 = out.cube2;
        data_snapshot.cube3 = out.cube3;
        data_snapshot.cube4 = out.cube4;
                
        all_sim_data{i} = data_snapshot;
        
        fprintf('Success.\n');
        
    catch ME
        fprintf('\nERROR at k=%d: %s\n', k_spring, ME.message);
        return;
    end
end

% plots
fprintf('\n=== PHASE 2: Generating Plots ===\n');

cube_colors = lines(4); 
k_styles = {'-', '--', ':'}; 
k_colors = {'b', 'r', 'k'};  

for i = 1:length(k_values)
    k_val = k_values(i);
    current_data = all_sim_data{i}; 
    
    fig = figure('Name', sprintf('Wave_Prop_k%d', k_val), 'Color', 'w', 'Visible', 'on');
    hold on; box on;
    
    plot(current_data.cube1.Time, current_data.cube1.Data, 'Color', cube_colors(1,:), 'LineWidth', 1.5, 'DisplayName', 'Cube 1');
    plot(current_data.cube2.Time, current_data.cube2.Data, 'Color', cube_colors(2,:), 'LineWidth', 1.5, 'DisplayName', 'Cube 2');
    plot(current_data.cube3.Time, current_data.cube3.Data, 'Color', cube_colors(3,:), 'LineWidth', 1.5, 'DisplayName', 'Cube 3');
    plot(current_data.cube4.Time, current_data.cube4.Data, 'Color', cube_colors(4,:), 'LineWidth', 1.5, 'DisplayName', 'Cube 4');
    
    xlabel('Time (s)'); ylabel('Position (m)');
    title(sprintf('Wave Propagation (k = %d N/m)', k_val));
    legend('Location', 'best'); grid on; xlim([0, 10]);
    
    saveas(fig, sprintf('Wave_Propagation_k%d.jpg', k_val));
end

cube_names = {'cube1', 'cube2', 'cube3', 'cube4'};

for c = 1:4
    c_name = cube_names{c};
    fig = figure('Name', sprintf('Stiffness_Comp_%s', c_name), 'Color', 'w', 'Visible', 'on');
    hold on; box on;
    
    for k_idx = 1:length(k_values)
        current_data = all_sim_data{k_idx};
        ts = current_data.(c_name); 
        
        plot(ts.Time, ts.Data, ...
             'LineStyle', k_styles{k_idx}, ...
             'Color', k_colors{k_idx}, ...
             'LineWidth', 1.5, ...
             'DisplayName', sprintf('k = %d', k_values(k_idx)));
    end
    
    xlabel('Time (s)'); ylabel('Position (m)');
    title(sprintf('Effect of Stiffness on %s', c_name));
    legend('Location', 'best'); grid on; xlim([0, 10]);
    
    saveas(fig, sprintf('Stiffness_Comparison_%s.jpg', c_name));
end