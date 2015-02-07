# last updated 2015-02-07 toby
library(ggplot2)
library(scales) # necessary for pretty_breaks

semtypes <- read.table("/home/toby/global_util/semtypes.txt",
	sep = "|", header = TRUE, stringsAsFactors = FALSE)

raw <- read.table("triple_types.txt", sep = "|", header = TRUE)

#-------------------------------------------------------------------------------

small <- data.frame(t_id = 1:nrow(raw), n_tup = raw$n_tup)

png(file = "semmed_uniq_tuples_by_triple_semtype.png", height = 1000, width = 1000)
ggplot(small, aes(x = t_id, y = log(n_tup))) +
	geom_point(shape = 1) +
	xlab(paste("Index of triple type (s_type, predicate, o_type)\n",
		"Total triple type combinations observed: 26229", sep = "")) +
	ylab("Log_e(Number of unique (s_cui, o_cui) tuples) for this type") +
	ggtitle("Number of unique (s_cui, o_cui) tuples with a specific semantic type from Semmeddb") +
	scale_x_continuous(breaks = pretty_breaks(n = 5)) +
	scale_y_continuous(breaks = pretty_breaks(n = 10))
dev.off()

temp <- data.frame(t_id = 1:nrow(raw), n_omim = raw$n_omim)

png(file = "omim_tuples_in_semmed.png", height = 1000, width = 1000)
ggplot(temp, aes(x = t_id, y = n_omim)) +
	geom_point(shape = 1) +
	xlab("Index of semmed triple semantic types (s_type, predicate, o_type)") +
	ylab("Number of OMIM tuples that can be found in this triple semtype subgroup") +
	ggtitle(paste0("Number of OMIM tuples that can be found in SEMMEDDB ",
		"broken into groups based on the triple semantic type")) +
	scale_x_continuous(breaks = pretty_breaks(n = 5))
dev.off()

#-------------------------------------------------------------------------------

# plot what the top triple semtypes are in human readable form

make_name <- function(s_type, pred, o_type)
{
	s_name <- semtypes[semtypes$code == s_type, "name"]
	o_name <- semtypes[semtypes$code == o_type, "name"]
	return (paste(c(s_name, pred, o_name), collapse = " "))
}

m <- 100 # only take these top hits (can't graph them all)

name <- unlist(apply(raw[1:m, ], 1, function(val)
{
	make_name(val["sub"], val["pred"], val["obj"])
}))

temp <- data.frame(trip = name, n_tup = raw$n_tup[1:m])

png(file = "top_semmed_triple_types.png", height = 2200, width = 1600)
ggplot(temp, aes(x = trip, y = n_tup)) +
	geom_bar(stat = "identity") +
	coord_flip() +
	scale_x_discrete(limits = name, labels = name) +
	ggtitle("Number of unique tuples grouped by triple semantic type for SEMMEDDB") +
	xlab("Semantic type of triple") +
	ylab("Number of unique (s_cui, o_cui) tuples")
dev.off()

#-------------------------------------------------------------------------------

# for triple types with at least one omim hit
# plot the absolute number of hits
# plot the ratio of hits to number of unique tuples

# find the triple types with at least one hit

small <- raw[raw$n_omim > 0, ]
name <- unlist(apply(small, 1, function(val)
{
	make_name(val["sub"], val["pred"], val["obj"])
}))

temp <- data.frame(trip_name = name, n_omim = small$n_omim,
	efficiency = small$n_omim / small$n_tup)

# plot absolute number of hits
temp <- temp[with(temp, order(-n_omim)), ]

png(file = "num_hits_per_triple_type.png", width = 1000, height = 1200)
ggplot(temp, aes(x = trip_name, y = n_omim)) +
	geom_bar(stat = "identity") +
	coord_flip() +
	scale_x_discrete(limits = temp$trip_name, labels = temp$trip_name) +
	ggtitle(paste0("Number of OMIM hits found in SEMMED grouped by triple semantic type\n",
		"for triple types with at least one hit")) +
	xlab("Triple semantic type (total types: 107)") +
	ylab("Number of unique OMIM tuple hits")
dev.off()

# plot hits per tuple
temp <- temp[with(temp, order(-efficiency)), ]

png(file = "efficiency_per_triple_type.png", width = 1000, height = 1200)
ggplot(temp, aes(x = trip_name, y = efficiency)) +
	geom_bar(stat = "identity") +
	coord_flip() +
	scale_x_discrete(limits = temp$trip_name, labels = temp$trip_name) +
	ggtitle(paste0("Number of OMIM hits divided by number of unique tuples\n",
		"for SEMMED triple semantic types with at least one OMIM hit")) +
	xlab("Triple semantic type (total types: 107)") +
	ylab("Number of unique OMIM hits / number of unique tuples")
dev.off()
