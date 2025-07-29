
### Fixed

- When reading assets, events, sequences, etc. using
`neat.read.cdf.classic...`. The conversion of label to tags no longer
changes non-alpha numeric characters. For example, if you had a label
`工事` it would previous be changed by neat to `%E5%B7%A5%E4%BA%8B'. This
is now fixed.