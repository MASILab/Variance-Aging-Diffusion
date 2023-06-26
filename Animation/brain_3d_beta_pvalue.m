clc
clear

path_cmap_folder = "/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Animation/cmap/";
myFiles = dir(fullfile(path_cmap_folder,'*.csv'));

for i = 1:length(myFiles)
    fn_csv = myFiles(i).name;
    
    % parse file name
    fn_csv_split = split(fn_csv,"-");
    atlas = fn_csv_split{1};
    measure = fn_csv_split{2};
    
    if fn_csv_split{3}=="beta"
        stat = "beta";
    elseif fn_csv_split{3}=="p"
        stat = "p-value";
    end
    last_split = split(fn_csv_split{length(fn_csv_split)}, ".");
    variable = last_split{1};
   
    
    % SELECT ONLY 1 ATLAS FOR TESTING
    if atlas ~= "EveType1" || stat ~= "beta" ||variable ~="Motion" || measure ~= "FA_std"
        continue
    end


    % location of the atlas
    if atlas== "EveType1"
        path_atlas = "/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Animation/atlas/JHU_MNI_SS_WMPM_Type-I.nii.gz";
        arr_axis = [18 205 15 165 0 157];
    elseif atlas == "EveType2"
        path_atlas = "/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Animation/atlas/JHU_MNI_SS_WMPM_Type-II.nii.gz";
        arr_axis = [18 205 15 165 0 157];
    elseif atlas == "EveType3"
        path_atlas = "/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Animation/atlas/JHU_MNI_SS_WMPM_Type-III.nii.gz";
        arr_axis = [18 205 15 165 0 157];
    elseif atlas == "BrainColor"
        path_atlas = "/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Animation/atlas/SLANT/output/FinalResult/JHU_MNI_SS_T1_seg.nii.gz";
        arr_axis = [16 207 14 166 4 156];
    end

    % Load atlas image
    img_atlas = niftiread(path_atlas);
    hdr_atlas = niftiinfo(path_atlas);     
    
    % Load cmap dataframe
    df_cmap = readtable(fullfile(path_cmap_folder, fn_csv));

    % RGB and alpha
    clr = table2array(df_cmap(:,3:5)); % R,G,B values
    alpha = table2array(df_cmap(:,6)); % alpha values

 
    % Plot region by region
    figure(1); clf; set(gcf, 'Position', [100 100 1600 1600]);
    xlabel("x")
    ylabel("y")
    zlabel("z")
    for j=1:size(df_cmap,1)
        disp([j size(df_cmap,1) alpha(j)])
        disp([atlas measure stat variable])
        
        roi_id = table2array(df_cmap(j,1));
        
        s = isosurface(smooth3(img_atlas==roi_id),0);
%         p = patch(reducepatch(reducepatch(s,0.2),0.2));
        p = patch(s);
        set(p,'edgecolor','none','FaceColor',clr(j,:),'facealpha',alpha(j))
        hold on
        drawnow

    end
    
    % axis range/ratio
    axis(arr_axis);
    daspect(1./hdr_atlas.PixelDimensions)
    axis off
 
    % Background: white
    set(gcf,'color','w', 'Position', [100 100 1600 1600])

    % Initial view angle
    view(40,30);
    
    set(gca,'CameraViewAngleMode','Manual');
   
%     % Light combo 1: 1 inside, 2 outside
%     lt_in = light("Color", [1,1,1], "Style", "local", "Position", [(arr_axis(1)+arr_axis(2))*0.5 (arr_axis(3)+arr_axis(4))*0.5 (arr_axis(5)+arr_axis(6))*0.5]);
%     lt_out1 = light("Color", [1,1,1], "Style", "local", "Position", [arr_axis(1) arr_axis(3) arr_axis(5)]);
%     lt_out2 = light("Color", [1,1,1], "Style", "local", "Position", [arr_axis(2) arr_axis(4) arr_axis(6)]);
     
 
%     % Light combo 2: 2 outside
%     lt_out1 = light("Color", [1,1,1], "Style", "local", "Position", [arr_axis(1) arr_axis(3) arr_axis(5)]);
%     lt_out2 = light("Color", [1,1,1], "Style", "local", "Position", [arr_axis(2) arr_axis(4) arr_axis(6)]);

%     % Light combo 3: 1 inside, 3 outside (a little far away)
%     lt_in = light("Color", [1,1,1], "Style", "local", "Position", [(arr_axis(1)+arr_axis(2))*0.5 (arr_axis(3)+arr_axis(4))*0.5 (arr_axis(5)+arr_axis(6))*0.5]);
%     lt_out1 = light("Color", [1,1,1], "Style", "local", "Position", [250 -10 200]);
%     lt_out2 = light("Color", [1,1,1], "Style", "local", "Position", [-20 200 150]);
%     lt_out3 = light("Color", [1,1,1], "Style", "local", "Position", [0 0 -20]);

    % Light combo 4: 8 outside (8 corners, 40% brightness)
    lt_out1 = light("Color", [0.4,0.4,0.4], "Style", "local", "Position", [arr_axis(1) arr_axis(3) arr_axis(5)]);
    lt_out2 = light("Color", [0.4,0.4,0.4], "Style", "local", "Position", [arr_axis(1) arr_axis(3) arr_axis(6)]);
    lt_out3 = light("Color", [0.4,0.4,0.4], "Style", "local", "Position", [arr_axis(1) arr_axis(4) arr_axis(5)]);
    lt_out4 = light("Color", [0.4,0.4,0.4], "Style", "local", "Position", [arr_axis(1) arr_axis(4) arr_axis(6)]);
    lt_out5 = light("Color", [0.4,0.4,0.4], "Style", "local", "Position", [arr_axis(2) arr_axis(3) arr_axis(5)]);
    lt_out6 = light("Color", [0.4,0.4,0.4], "Style", "local", "Position", [arr_axis(2) arr_axis(3) arr_axis(6)]);
    lt_out7 = light("Color", [0.4,0.4,0.4], "Style", "local", "Position", [arr_axis(2) arr_axis(4) arr_axis(5)]);
    lt_out8 = light("Color", [0.4,0.4,0.4], "Style", "local", "Position", [arr_axis(2) arr_axis(4) arr_axis(6)]);

    camproj('perspective')
    lighting gouraud
    material shiny
    
    % Record videos
    OptionZ.FrameRate=60;OptionZ.Duration=20;OptionZ.Periodic=true;
    path_video_folder = "/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Animation/video/";
    path_video = fullfile(path_video_folder,append('EffectSize-of-',variable,'-on-',measure,'-',atlas,'-light4-whitebkgd'));
%     CaptureFigVid([-20,10;-110,10;-190,80;-290,10;-380,10], path_video,OptionZ)
    
%     % Add annotations
%     len_extend = [50 50 25];
%     space_text = 10;
%     arr_axis = [arr_axis(1)-len_extend(1), arr_axis(2)+len_extend(1), ...
%                 arr_axis(3)-len_extend(2), arr_axis(4)+len_extend(2), ...
%                 arr_axis(5)-len_extend(3), arr_axis(6)+len_extend(3)];
%     axis(arr_axis);
%     
%     plot3([arr_axis(1)+space_text arr_axis(2)-space_text],...
%           [0.5*(arr_axis(3)+arr_axis(4)) 0.5*(arr_axis(3)+arr_axis(4))],...
%           [0.5*(arr_axis(5)+arr_axis(6)) 0.5*(arr_axis(5)+arr_axis(6))], '--k', 'LineWidth', 3)
%     plot3([0.5*(arr_axis(1)+arr_axis(2)) 0.5*(arr_axis(1)+arr_axis(2))],...
%           [arr_axis(3)+space_text arr_axis(4)-space_text],...
%           [0.5*(arr_axis(5)+arr_axis(6)) 0.5*(arr_axis(5)+arr_axis(6))], '--k', 'LineWidth', 3)
%     plot3([0.5*(arr_axis(1)+arr_axis(2)) 0.5*(arr_axis(1)+arr_axis(2))],...
%           [0.5*(arr_axis(3)+arr_axis(4)) 0.5*(arr_axis(3)+arr_axis(4))],...
%           [arr_axis(5)+space_text arr_axis(6)-space_text], '--k', 'LineWidth', 3)
%       
%     text(arr_axis(1), 0.5*(arr_axis(3)+arr_axis(4)), 0.5*(arr_axis(5)+arr_axis(6)), ...
%          'P', 'HorizontalAlignment', 'center', 'FontWeight', 'bold', 'FontSize', 28);
%     text(arr_axis(2), 0.5*(arr_axis(3)+arr_axis(4)), 0.5*(arr_axis(5)+arr_axis(6)), ...
%          'A', 'HorizontalAlignment', 'center', 'FontWeight', 'bold', 'FontSize', 28);
%     text(0.5*(arr_axis(1)+arr_axis(2)), arr_axis(3), 0.5*(arr_axis(5)+arr_axis(6)), ...
%          'R', 'HorizontalAlignment', 'center', 'FontWeight', 'bold', 'FontSize', 28);
%     text(0.5*(arr_axis(1)+arr_axis(2)), arr_axis(4), 0.5*(arr_axis(5)+arr_axis(6)), ...
%          'L', 'HorizontalAlignment', 'center', 'FontWeight', 'bold', 'FontSize', 28);
%     text(0.5*(arr_axis(1)+arr_axis(2)), 0.5*(arr_axis(3)+arr_axis(4)), arr_axis(5), ...
%          'I', 'HorizontalAlignment', 'center', 'FontWeight', 'bold', 'FontSize', 28);
%     text(0.5*(arr_axis(1)+arr_axis(2)), 0.5*(arr_axis(3)+arr_axis(4)), arr_axis(6), ...
%          'S', 'HorizontalAlignment', 'center', 'FontWeight', 'bold', 'FontSize', 28);
    
     % Take screenshots
     for elevation = [-90, 0, 90]
         for azimuth = [0, 90, 180, 270]
             view(azimuth,elevation);
             if exist(path_video, 'dir') ~= 7
                 mkdir(path_video);
             end
             filename = fullfile(path_video,...
                 append('EffectSize-of-',variable,'-on-',measure,'-',atlas,'-light4-whitebkgd-screenshot-e_',num2str(elevation),'-a_',num2str(azimuth),'.png'));
             saveas(gcf, filename);
         end
     end
    
    break
end