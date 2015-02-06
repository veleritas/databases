# last updated 2015-02-06 toby
library(ggplot2)
library(scales)

raw <- read.table("triple_types.txt", sep = "|", header = FALSE)
names(raw) <- c("sub", "pred", "obj", "n_trip", "n_omim")

print(head(raw, 10))

lol <- data.frame(t_id = 1:nrow(raw), n_trip = raw$n_trip)

print(head(lol))


png(file = "a.png", height = 1000, width = 1000)
ggplot(lol, aes(x=t_id, y=log(n_trip))) +
	geom_point(shape=1) +
	xlab(paste("Index of triple type (s_type, predicate, o_type)\n",
		"Total triple type combinations observed: 26229", sep = "")) +
	ylab("Log_e(Number of unique triples of this type") +


	ggtitle("Number of unique triples with a specific semantic type from Semmeddb") +
	scale_x_continuous(breaks = pretty_breaks(n = 5)) +
	scale_y_continuous(breaks = pretty_breaks(n = 10))




dev.off()






## Make some noisily increasing data
#dat <- data.frame(cond = rep(c("A", "B"), each=10),
#                  xvar = 1:20 + rnorm(20,sd=3),
#				                    yvar = 1:20 + rnorm(20,sd=3))
## cond         xvar         yvar
##    A -4.252354091  3.473157275
##    A  1.702317971  0.005939612
##   ... 
##    B 17.793359218 19.718587761
##    B 19.319909163 19.647899863
#
#
#
#
#
#
#print(head(dat))
#
#png(file = "lol.png", height = 1000, width = 1000)
#ggplot(dat, aes(x=xvar, y=yvar)) +
#	geom_point(shape=1)
#
#dev.off()






#-------------------------------------------------------------------------------

#png(file = "num_triple_semtypes.png", height = 1000, width = 1000)
#plot(log(raw$n_trip),
#	main = "Number of unique triples with a specific semantic type from semmeddb",
#	xlab = "Total number of (s_type, predicate, o_type) combinations observed: 26229",
#	ylab = "Log_e(number of unique triples with this type)")
#dev.off()
#
#png(file = "triples_in_omim.png", height = 1000, width = 1000)
#plot(raw$n_omim,
#	main = "Number of tuple hits in omim for a specific triple semantic type from semmeddb",
#	xlab = "Total number of (s_type, predicate, o_type) combinations observed: 26229",
#	ylab = "Number of hits in omim for this specific triple semantic type",
#	col = ifelse(as.numeric(raw$n_omim) > 0, "red", "blue"))
#dev.off()
#
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
