library(tidyverse)
library(lme4)
library(lmerTest)

library(readr)
library(ggplot2)

# Read csv
brain_stats <- read_csv("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_Brain_stats_concat_20221110_delivery.csv")
motion_stats <- read_csv("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_eddy_movement_rms_average_20221109.csv")

################### DATA PREPARATION ###################
# SELECT WHICH TO ANALYZE
s_atlas = 'EveType1'
s_region_id = '140'
s_measure = 'FA_std'

# Create DataFrame based on motion_stats
df <- motion_stats[c("Subject_ID","Session","DTI_ID","Sex","Age","Motion")]

# Drop the NA rows where Age info is missing
df <- df[!is.na(df$Age),]

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
    for (i in 1:nrow(brain_stats)) {
      ses <- brain_stats['Session'][[1]][i]
      val <- brain_stats[col][[1]][i]
      
      df[(df$Session==ses)&(df$DTI_ID==dti_id), s_measure] <- val
    }
  }
}

# Drop the NA rows where measure value is missing
df <- df[!is.na(df[s_measure]),]

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
fn_save = sprintf("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/part/%s-%s-%s.csv", s_atlas, s_region_id, s_measure)
write.csv(df, fn_save, row.names=FALSE, quote=FALSE)

################### LINEAR MIXED EFFECTS MODEL ###################
# convert to factor class variables
df <- within(df, {
  Subject_ID <- factor(Subject_ID)
  DTI_ID <- factor(DTI_ID)
  Sex <- factor(Sex)
})

## Backward regression
# Start with full model and do backward regression
m <- lmer(FA_std ~ Age_base + Interval + Interval_sqr + Motion + Sex + DTI_ID + (1 + Interval | Subject_ID), data = df, REML=TRUE)
s <- step(m)
print(s)

# Manually
# Manual selection by Likelihood ratio test
m1 <- lmer(FA_std ~ Age + (1 | Subject_ID), data=df, REML=FALSE)
m2 <- lmer(FA_std ~ Age + Sex + (1 | Subject_ID), data=df, REML=FALSE)
anova(m1, m2) # logLik increased! Preserve "Sex"

m3 <- lmer(FA_std ~ Age + Sex + Motion + (1 | Subject_ID), data=df, REML=FALSE)
anova(m2, m3) # logLik doesn't change much. Remove "Motion"

m4 <- lmer(FA_std ~ Age + Sex + DTI_ID + (1 | Subject_ID), data=df, REML=FALSE)
anova(m2, m4) # logLik increased! Preserve "DTI_ID"

# verify that m5 and m6 should be no difference, because you can get the other by linear combination
m5 <- lmer(FA_std ~ Age + Age_base + Sex + DTI_ID + (1 | Subject_ID), data=df, REML=FALSE)
anova(m4, m5)
m6 <- lmer(FA_std ~ Age + Interval + Sex + DTI_ID + (1 | Subject_ID), data=df, REML=FALSE)
anova(m5, m6)
m7 <- lmer(FA_std ~ Age_base + Interval + Sex + DTI_ID + (1 | Subject_ID), data=df, REML=FALSE)
anova(m5, m7)

# what about adding "Motion" again now?
m8 <- lmer(FA_std ~ Age_base + Interval + Sex + DTI_ID + Motion + (1 | Subject_ID), data=df, REML=FALSE)
anova(m7, m8) # Still doesn't change much. Remove "Motion"

# add random slope to the "Subject_ID", the first two cannot converge, while the third one can
# One guess for the reason is that using the interval acts like normalization, making the data distribution to the center.
#m9 <- lmer(FA_std ~ Age_base + Interval + Sex + DTI_ID + (1 + Age | Subject_ID), data=df, REML=FALSE)
#m9 <- lmer(FA_std ~ Age_base + Interval + Sex + DTI_ID + (1 + Age_base | Subject_ID), data=df, REML=FALSE)
m9 <- lmer(FA_std ~ Age_base + Interval + Sex + DTI_ID + (1 + Interval | Subject_ID), data=df, REML=FALSE)
anova(m7, m9)
summary(m9)

# add "Motion" again?
m9.wmotion<- lmer(FA_std ~ Age_base + Interval + Sex + DTI_ID + Motion + (1 + Interval | Subject_ID), data=df, REML=FALSE)
anova(m9, m9.wmotion) # doesn't change much, remove

# Use restricted maximum likelihood to fit the model
m9.reml <- lmer(FA_std ~ Age_base + Interval + Sex + DTI_ID + (1 + Interval | Subject_ID), data=df, REML=TRUE)
summary(m9.reml)

# Add a new column
df['Interval_sqr'] <- df['Interval']^2
m10 <- lmer(FA_std ~ Age_base + Interval + Interval_sqr + Sex + DTI_ID + (1 + Interval | Subject_ID), data=df, REML=FALSE)
anova(m9, m10)

# Rethink: Interval_sqr is not necessary. Our goal is not only to fit the data well, but also to explain the coefficients

library(report)
report(m9.reml)
report(sessionInfo())
report_statistics(m9.reml)
report_model(m9.reml)
report_text(m9.reml)
report_table(m9.reml)

library("insight")
t <- report_table(m9.reml)
display(t)

model_info(m9.reml)
