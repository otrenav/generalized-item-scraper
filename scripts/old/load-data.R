#
# Load site data into data frame
#

FILE_EXTENSION <- "csv"
OUTPUTS_DIRECTORY <- "../outputs/"

full_file_name <- function(file) {
    paste(OUTPUTS_DIRECTORY, file, sep = "")
}

load_site_data <- function() {
    print("Loading CSV files...")
    files <- list.files(OUTPUTS_DIRECTORY, pattern = "*.csv")
    data <- NULL
    for (file in files) {
        full_file_name <- full_file_name(file)
        print(paste("   ", full_file_name))
        data <- rbind(data, read.csv(full_file_name))
    }
    print("Done.")
    return(data)
}

#
# Usage example
#
# NOTE: Data needs post-processing for analysis,
#       but this is how you can load it.
#

data <- load_site_data()

str(data)
head(data)
