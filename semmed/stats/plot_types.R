# last updated 2015-02-06 toby
library(ggplot2)
library(scales) # necessary for pretty_breaks

semtypes <- read.table("/home/toby/global_util/semtypes.txt",
	sep = "|", header = TRUE, stringsAsFactors = FALSE)
print(head(semtypes))

raw <- read.table("triple_types.txt", sep = "|", header = TRUE)

#print(head(raw, 10))

#-------------------------------------------------------------------------------

#small <- data.frame(t_id = 1:nrow(raw), n_tup = raw$n_tup)
#
#png(file = "semmed_uniq_tuples_by_triple_semtype.png", height = 1000, width = 1000)
#ggplot(small, aes(x = t_id, y = log(n_tup))) +
#	geom_point(shape = 1) +
#	xlab(paste("Index of triple type (s_type, predicate, o_type)\n",
#		"Total triple type combinations observed: 26229", sep = "")) +
#	ylab("Log_e(Number of unique (s_cui, o_cui) tuples) for this type") +
#	ggtitle("Number of unique (s_cui, o_cui) tuples with a specific semantic type from Semmeddb") +
#	scale_x_continuous(breaks = pretty_breaks(n = 5)) +
#	scale_y_continuous(breaks = pretty_breaks(n = 10))
#dev.off()
#
#temp <- data.frame(t_id = 1:nrow(raw), n_omim = raw$n_omim)
#
#png(file = "omim_tuples_in_semmed.png", height = 1000, width = 1000)
#ggplot(temp, aes(x = t_id, y = n_omim)) +
#	geom_point(shape = 1) +
#	xlab("Index of semmed triple semantic types (s_type, predicate, o_type)") +
#	ylab("Number of OMIM tuples that can be found in this triple semtype subgroup") +
#	ggtitle(paste0("Number of OMIM tuples that can be found in SEMMEDDB ",
#		"broken into groups based on the triple semantic type")) +
#	scale_x_continuous(breaks = pretty_breaks(n = 5))
#dev.off()

#-------------------------------------------------------------------------------

# plot what the top triple semtypes are in human readable form

make_name <- function(s_type, pred, o_type)
{
	s_name <- semtypes[semtypes$code == s_type, "name"]
	o_name <- semtypes[semtypes$code == o_type, "name"]
	return (paste(c(s_name, pred, o_name), collapse = " "))
}

m <- 100

name <- unlist(apply(raw[1:m, ], 1, function(val)
{
	make_name(val["sub"], val["pred"], val["obj"])
}))

temp <- data.frame(trip = name, n_tup = raw$n_tup[1:m])
print(head(temp))



png(file = "top_semmed_triple_types.png", height = 2200, width = 2000)

ggplot(temp, aes(x = trip, y = n_tup)) +
	geom_bar(stat = "identity") +
	coord_flip() +
	scale_x_discrete(limits = name, labels = name)

dev.off()


#par(las = 1, mar = par('mar') + c(0, 33, 0, 0))
#
#barplot(raw$n_tup[1:m], names.arg = name,
#	horiz = TRUE, xlab = "Number of unique tuples with this type",
#	main = "Top 100 semantic types of unique triples found in SEMMEDDB")
#dev.off()
#
#print(sum(raw$num))







##-------------------------------------------------------------------------------
#
#print(sum(raw$n_omim))
#
#omim <- Filter(function(x) x > 0, raw$n_omim)
#print(head(omim))
#
#small <- raw[raw$n_omim > 0,  ] # get all info where we got at least one omim hit
#print(head(small))
#
#
#make_name <- function(s_type, pred, o_type)
#{
#	return (paste(c(s_type, pred, o_type), collapse = " "))
#}
#
#
#name <- unlist(apply(small[1:nrow(small), ], 1, function(val)
#{
#	make_name(val["sub"], val["pred"], val["obj"])
#}))
#
#png(file = "omim_hit_semtypes.png", height = 1600, width = 1000)
#par(las = 1, mar = par('mar') + c(0, 20, 0, 0))
#barplot(small$n_trip, names.arg = name,
#	horiz = TRUE, xlab = "Number of unique triples with this type",
#	main = "Triple semantic types for which at least one OMIM hit was found")
#dev.off()

#
#
#
#
#
#
#png(file = "num_omim_hit_semtypes.png", height = 1600, width = 1000)
#par(las = 1, mar = par('mar') + c(0, 20, 0, 0))
#barplot(small$n_omim, names.arg = name,
#	horiz = TRUE, xlab = "Number of omim hits for this triple type",
#	main = "Number of omim hits for triple semantic types for which at least one hit was found")
#dev.off()

#-------------------------------------------------------------------------------



#m <- min(nrow(raw), 100)
#print(m)

#name <- unlist(apply(raw[1:m, ], 1, function(val)
#{
#	make_name(val["sub"], val["pred"], val["obj"])
#}))
#
#
#png(file = "n_human_top_semmed_triple_types.png", height = 2000, width = 1800)
#par(las = 1, mar = par('mar') + c(0, 33, 0, 0))
#
#barplot(raw$num[1:m], names.arg = name,
#	horiz = TRUE, xlab = "Number of unique triples with this type",
#	main = "Top 100 semantic types of unique triples found in SEMMEDDB")
#dev.off()
#
#
#print(sum(raw$num))
