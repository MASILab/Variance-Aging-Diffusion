library(readr)

# Read csv
brain_stats <- read_csv("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_Brain_stats_concat_20221110_delivery.csv")
motion_stats <- read_csv("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_eddy_movement_rms_average_20221109.csv")

# Select which to analyze
s_atlas = 'EveType1'
s_region_id = '140'
s_measure = 'FA_std'


# Create DataFrame based on motion_stats
df <- motion_stats[c("Subject_ID","Session","DTI_ID","Sex","Age","Motion")]

# New column: Age at baseline visit
df["Age_base"] <- NA

list_subject <- unique(unlist(df$Subject_ID))

for (sub in list_subject) {
  age_baseline <- min(df[df$Subject_ID == sub, "Age"])
  df[df$Subject_ID == sub, "Age_base"] <- age_baseline
} 

# New column: Interval (Age - Age_base)
df['Interval'] <- df['Age'] - df['Age_base']

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
      dti_id = 0
      next
    } else {
      print("Error DTI_ID!")
    }
  } else {
  print("Error: measure type!")
  }
  
  if (atlas == s_atlas & region_id == s_region_id & measure == s_measure) {
    
    print(col)
    print(c(atlas, region_id, measure, dti_id))
    
    for (i in 1:nrow(brain_stats)) {
      
      ses <- brain_stats['Session'][[1]][i]
      val <- brain_stats[col][[1]][i]
      
      df[(df$Session == ses & df$DTI_ID ==dti_id), s_measure] <- val
    }
  }
}

nrow(df[!is.na(df$FA_std)&!is.na(df$Age),])

nrow(df)
nrow(motion_stats)
nrow(df[complete.cases(df),])
summary(motion_stats)
summary(df)
View(df)
