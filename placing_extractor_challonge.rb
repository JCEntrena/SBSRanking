#!/usr/bin/env ruby
#encoding: utf-8

######################################
# Extracting data from Challonge.
######################################

require 'challonge-api'

# Set params.
Challonge::API.username = 'SmashBrosSpain'
Challonge::API.key = 'TYd05AbGSdR2WuEp1dtfmhPSimChv6cGOOJuRebE' # KEEP PRIVATE

# Season dates
@season_begin = Date.new(2017, 8, 26)
@season_end = Date.new(2018, 2, 24)

# Get tournaments.
tournaments = Challonge::Tournament.find(:all)
# Remove tournaments of other seasons.
tournaments.select!{|x| x.completed_at != nil}
tournaments.select!{|x| Date.parse(x.completed_at) <= @season_end and Date.parse(x.completed_at) >= @season_begin}

tournaments.each do |tournament|
  # Get name (for data files names)
  name = tournament.name.clone
  name.tr!(' ', '')
  # Participants and placings.
  placings = []
  tournament_participants = []
  tournament.participants.each do |player|
    placings << [player.name.clone, player.final_rank]
  end

  # File for writing
  file = File.new('./Data/placings_' + name + '.txt', "w+")

  # Writing
  placings.each do |player|
    file.write(player.join(' ') + "\n")
  end

end
