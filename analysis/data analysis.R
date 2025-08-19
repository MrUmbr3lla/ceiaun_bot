library(openxlsx)
library(dplyr)
library(readxl)
library(ggplot2)


# List of file paths
file_paths <- c("#add your file path/paths here")



wrong_inputs <- c("ریاضی", "معادلات", "دیفرانسیل" , "ریاضی2" , "محاسبه" , "زبان" , "ریاضی۲")



# Create an empty data frame to store merged data
merged_data <- data.frame()


# Load and clean datasets
for (i in 1:length(file_paths)) {
  # Read data
  assign(paste0("X2_", i), read_excel(file_paths[i]))


  # Filter out wrong inputs and make data unique
  cleaned_data <- get(paste0("X2_", i)) %>%
    filter(!grepl("%", .[[3]]) | is.na(.[[3]])) %>%
    distinct()


  # Merge the cleaned data with the previous datasets
  merged_data <- rbind(merged_data, cleaned_data)
}


# Function to check if any of the words are present in a string
contains_words <- function(text, words) {
  any(sapply(words, function(word) {
    grepl(paste0("\\b", word, "\\b"), text, ignore.case = TRUE)
  }))
}


# Apply the filtering function to remove rows with specific words in column 3
merged_data <- merged_data %>%
  filter(!sapply(merged_data[[3]], function(text) contains_words(text, wrong_inputs)))
View(merged_data)


# Save merged data to a single sheet in an Excel file
write.xlsx(merged_data, file = "#add your file path here")
