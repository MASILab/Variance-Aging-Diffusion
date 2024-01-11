# In this version, FA/RD/MD/AD values are z-scored before feeding to the Linear Mixed-effects model.

library(tidyverse)
library(lme4)
library(lmerTest)
library(readr)
library(ggplot2)

# Load data
brain_stats <- read_csv("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_Brain_stats_concat_20221110_delivery.csv")
motion_stats <- read_csv("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_eddy_movement_rms_average_20221109.csv")

# list of regions/measurements/values
list_atlas <- c('EveType1','EveType2','EveType3','BrainColor')
list_diff_type <- c('RD', 'AD', 'FA', 'MD')
list_value_type <- c('std')

for (s_atlas in list_atlas) {
  # load the look up table
  path_LUT = sprintf("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_customize/%s_LUT.csv", s_atlas)
  LUT <- read_csv(file=path_LUT)
  
  # loop through region IDs
  for (idx_region in 1:nrow(LUT)) {
    for (diff_type in list_diff_type) {
      for (value_type in list_value_type) {
        ######################### Main code starts here #######################
        print(sprintf("%s  %s  %s  %s", s_atlas,idx_region,diff_type,value_type))
        
        s_region_id = as.character(LUT$id[idx_region])
        s_measure <- paste(diff_type, value_type, sep='_') # eg, FA_std
        
        # Data preparation
        df <- motion_stats[c("Subject_ID", "Session", "DTI_ID", "Sex", "Age", "Motion")]
        
        # Drop the NA rows where Age info is missing
        df <- df[!is.na(df$Age), ]
        
        # New column: selected measure
        df[s_measure] = NA
        
        for (col in names(brain_stats)){
          # skip the session column
          if (col == 'Session'){
            next
          }
          
          # parse the column name
          region <- strsplit(x=col, split=" ")[[1]][1]  # "BrainColor-207"
          atlas <- strsplit(x=region, split="-")[[1]][1] # "BrainColor"
          region_id <- strsplit(x=region, split="-")[[1]][2] # "207"
          
          if (grepl("-Volume", col, fixed=TRUE)) {
            measure <- 'volume'
            next
          } else if (grepl("-mean", col, fixed=TRUE) | grepl("-std", col, fixed=TRUE)) {
            col_parts = strsplit(x=col, split='-')[[1]]
            measure <- paste(col_parts[length(col_parts)-1], col_parts[length(col_parts)], sep="_")
            
            # DTI1 or DTI2?
            if (grepl("DTI1", col, fixed=TRUE)) {
              dti_id = 1
            } else if (grepl("DTI2", col, fixed=TRUE)) {
              dti_id = 2
            } else if (grepl("DTI_double", col, fixed=TRUE)) {
              dti_id = NA
              next
            } else {
              print("Error: DTI_ID!")
            }
          } else {
            print("Error: measure type!")
          }
          
          if (atlas == s_atlas & region_id == s_region_id & measure == s_measure) {
            for (idx_row in 1:nrow(brain_stats)) {
              ses <- brain_stats['Session'][[1]][idx_row]
              val <- brain_stats[col][[1]][idx_row]
              
              df[(df$Session==ses)&(df$DTI_ID==dti_id), s_measure] <- val
            }
          }
        }
        
        # Drop the NA rows where measure value is missing
        df <- df[!is.na(df[s_measure]),]
        
        # Z-score the column of measure values
        df[s_measure] <- (df[s_measure] - mean(df[[s_measure]])) / sd(df[[s_measure]])
        
        # New column: Age at baseline visit
        df["Age_base"] <- NA
        
        list_subject <- unique(unlist(df$Subject_ID))
        for (sub in list_subject) {
          age_baseline <- min(df[df$Subject_ID == sub, "Age"])
          df[df$Subject_ID == sub, "Age_base"] <- age_baseline
        } 
        
        # New column: Interval, time since first visit
        df['Interval'] <- df['Age'] - df['Age_base']
        
        # Re-order and save
        df <- df[c("Subject_ID", "Sex", "Session", "DTI_ID", "Age", "Age_base", "Interval", "Motion", s_measure)]
        fn_save = sprintf("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_zscore_feature_20230208/part/%s-%s-%s.csv", s_atlas, s_region_id, s_measure)
        write.csv(df, fn_save, row.names=FALSE, quote=FALSE)
        
        # LINEAR MIXED-EFFECTS MODEL
        # Subject_ID, DTI_ID, Sex: convert numeric to factor
        df <- within(df, {
          Subject_ID <- factor(Subject_ID)
          DTI_ID <- factor(DTI_ID)
          Sex <- factor(Sex)
        })
        
        # Backward regression
        formula_full_model <- sprintf("%s ~ Age_base + Interval + Motion + Sex + DTI_ID + (1 | Subject_ID)", s_measure)
        m <- lmer(formula_full_model, data = df, REML = TRUE)
        s <- step(m,reduce.fixed=TRUE, reduce.random=FALSE)
        m_final <- get_model(s)
        
        # Save results
        coef_df <- as.data.frame(coef(m_final)$Subject_ID)
        fn_save <- sprintf("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_zscore_feature_20230208/stats/coef_ind/%s-%s-%s_coef.csv", s_atlas, s_region_id, s_measure)
        write.csv(coef_df, fn_save, row.names=TRUE, quote=FALSE)
        
        coef_sum_df <- as.data.frame(coef(summary(m_final)))
        fn_save <- sprintf("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_zscore_feature_20230208/stats/coef_sum/%s-%s-%s_coef_summary.csv", s_atlas, s_region_id, s_measure)
        write.csv(coef_sum_df, fn_save, row.names=TRUE, quote=FALSE)
        
        ranef_df <- as.data.frame(ranef(m_final)$Subject_ID)
        fn_save <- sprintf("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_zscore_feature_20230208/stats/ranef_ind/%s-%s-%s_ranef.csv", s_atlas, s_region_id, s_measure)
        write.csv(ranef_df, fn_save, row.names=TRUE, quote=FALSE)
        
        ranef_sum_df <- as.data.frame(VarCorr(m_final))
        ranef_sum_df <- ranef_sum_df[c('grp','vcov','sdcor')]
        colnames(ranef_sum_df) <- c("Groups","Variance","std")
        fn_save <- sprintf("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_zscore_feature_20230208/stats/ranef_sum/%s-%s-%s_ranef_summary.csv", s_atlas, s_region_id, s_measure)
        write.csv(ranef_sum_df, fn_save, row.names=TRUE, quote=FALSE)
        
        ######################### Main code ends here #######################
      }
    }
  } 
}


