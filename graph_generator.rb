#!/usr/bin/env ruby
#encoding: utf-8

############################
# Graph generator.
############################

# Data structures.
data = []
players = []
# Files to write.

# Reading data
Dir.foreach('./ExtractedData') do |item|
  # Not working over '.' and '..'
  next if item == '.' or item == '..' or item == 'Results'
  # Working on real data files.
  # Opening the file in Data/file
  file = File.new('./ExtractedData/' + item, "r")
  file.gets
  file.gets
  iter = file.gets.to_i
  file.gets
  iter.times do |i|
    line = file.gets
    # All in lower case
    data << line.split(' ').map{|x| x.downcase}
    players << line.split(' ').first.downcase
  end
end
# Remove nested list structure.
players.flatten!
# Remove repeated
players.uniq!
# Sort
players.sort!

# Replace player with number.
data.each do |set|
  (0..1).each do |i|
    set[i] = players.index(set[i])
  end
end

# Write data
#file = File.new('./Data/Results/graph.txt', "w+")
#data.each do |set|
#  file.write(set.join(' ') + "\n")
#end

file = File.new('./Data/Results/players2.txt', "w+")
players.each_with_index do |player, index|
  file.write(player + ' ' + index.to_s + "\n")
end
