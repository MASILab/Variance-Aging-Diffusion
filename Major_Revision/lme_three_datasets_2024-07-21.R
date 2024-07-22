# Linear mixed-effects models using BLSA, BIOCARD, and ADNI.
# FA_std ~ Age_base + Interval + motion + sex + (1 | subject) + (1 | site)
# 
# Author: Chenyu Gao
# Date: July 21, 2024

library(tidyverse)
library(lme4)
library(lmerTest)
library(readr)
library(ggplot2)
library(optimx)

# Load data and look-up table
df <- read_csv("OneDrive - Vanderbilt/Research/MASI/Projects/Diffusion_MRI_Variance_Aging/Major_Revision/experiments/data_site_motion_fa-std_snr.csv")
lut <- read_csv("OneDrive - Vanderbilt/Research/MASI/Projects/Diffusion_MRI_Variance_Aging/Major_Revision/experiments/EveType1_LUT.csv")

df <- df[!is.na(df$age), ]

# Create columns. Age_base: Age at baseline visit. Interval: time since first visit. Both in decades.
df["Age_base"] <- NA

list_subject <- unique(unlist(df$subject))
for (sub in list_subject) {
  age_baseline <- min(df[df$subject == sub, "age"])
  df[df$subject == sub, "Age_base"] <- age_baseline
} 

df['Interval'] <- df['age'] - df['Age_base']
df['Interval'] <- df['Interval']/10
df['Age_base'] <- df['Age_base']/10

# Loop through ROIs and perform LME
for (idx in 1:nrow(lut)) {
  idx_roi = lut$id[idx]
  measure_col = sprintf("EveType1-%s-FA_std", idx_roi)
  data <- df[c("subject", "session", "sex", "site", "motion", "Age_base", "Interval", measure_col)]
  data <- na.omit(data)
  
  # Z-score the measurement values
  measure_z_col = sprintf("EveType1-%s-FA_std-zscore", idx_roi)
  data[measure_z_col] <- (data[measure_col] - mean(data[[measure_col]])) / sd(data[[measure_col]])
  save_csv = sprintf("OneDrive - Vanderbilt/Research/MASI/Projects/Diffusion_MRI_Variance_Aging/Major_Revision/experiments/part/EveType1-%s-FA_std.csv", as.character(idx_roi))
  write.csv(data, save_csv, row.names=FALSE, quote=FALSE)
  
  # Linear mixed-effects models
  data["y"] <- data[measure_z_col]
  data <- within(data, {
    subject <- factor(subject)
    site <- factor(site)
    sex <- factor(sex)
  })
  
  formula_full_model <- "y ~ Age_base + Interval + motion + sex + (1 | subject) + (1 | site)"
  m <- lmer(formula_full_model, data = data, REML = TRUE, control = lmerControl(optimizer = "nloptwrap", optCtrl=list(maxfun=1e6)))
  s <- step(m, reduce.fixed=TRUE, reduce.random=FALSE)
  m_final <- get_model(s)
  
  # Save results
  coef_data <- as.data.frame(coef(m_final)$subject)
  save_csv <- sprintf("OneDrive - Vanderbilt/Research/MASI/Projects/Diffusion_MRI_Variance_Aging/Major_Revision/experiments/stats/coef_ind/EveType1-%s-FA_std_coef.csv", as.character(idx_roi))
  write.csv(coef_data, save_csv, row.names=TRUE, quote=FALSE)
  
  coef_sum_data <- as.data.frame(coef(summary(m_final)))
  save_csv <- sprintf("OneDrive - Vanderbilt/Research/MASI/Projects/Diffusion_MRI_Variance_Aging/Major_Revision/experiments/stats/coef_sum/EveType1-%s-FA_std_coef_summary.csv", as.character(idx_roi))
  write.csv(coef_sum_data, save_csv, row.names=TRUE, quote=FALSE)
  
  ranef_data <- as.data.frame(ranef(m_final)$subject)
  save_csv <- sprintf("OneDrive - Vanderbilt/Research/MASI/Projects/Diffusion_MRI_Variance_Aging/Major_Revision/experiments/stats/ranef_ind/EveType1-%s-FA_std_ranef.csv", as.character(idx_roi))
  write.csv(ranef_data, save_csv, row.names=TRUE, quote=FALSE)
  
  ranef_sum_data <- as.data.frame(VarCorr(m_final))
  ranef_sum_data <- ranef_sum_data[c('grp','vcov','sdcor')]
  colnames(ranef_sum_data) <- c("Groups","Variance","std")
  save_csv <- sprintf("OneDrive - Vanderbilt/Research/MASI/Projects/Diffusion_MRI_Variance_Aging/Major_Revision/experiments/stats/ranef_sum/EveType1-%s-FA_std_ranef_summary.csv", as.character(idx_roi))
  write.csv(ranef_sum_data, save_csv, row.names=TRUE, quote=FALSE)
  
  print(sprintf("%s / %s", idx, nrow(lut)))
}