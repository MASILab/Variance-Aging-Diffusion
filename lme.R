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

############################## TODO: Start from here
# LINEAR MIXED EFFECTS MODEL
# convert to factor class variables
df <- within(df, {
  Subject_ID <- factor(Subject_ID)
  DTI_ID <- factor(DTI_ID)
  Sex <- factor(Sex)
})
#
p <- ggplot(data = df[df$DTI_ID==1,], aes(x = Age, y = FA_std, group = Subject_ID))
p + geom_point()
p + geom_line() + facet_grid(. ~ Sex)
