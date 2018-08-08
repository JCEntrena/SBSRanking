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
@season_begin = Date.new(2018, 2, 25)
@season_end = Date.new(2018, 8, 6)

# Get tournaments.
tournaments = Challonge::Tournament.find(:all)
# Remove tournaments of other seasons.
tournaments.select!{|x| x.completed_at != nil}
tournaments.select!{|x| Date.parse(x.completed_at) <= @season_end and Date.parse(x.completed_at) >= @season_begin}

tournaments.each do |tournament|
  # Get name (for data files names)
  name = tournament.name.clone
  name.tr!(' ', '')
  # Participants.
  placings = []
  tournament_participants = []
  tournament.participants.each do |player|
    placings << [player.name.clone, player.final_rank]
    placings.sort!{|a, b| a[1] <=> b[1]}
    tournament_participants << [player.name.clone, player.id]
  end

  matches_list = tournament.matches.clone
  # Remove pools
  matches_list.select!{|match| match.group_id == nil}
  # Divide in winners and losers
  # Challonge has negative round number for sets in losers.
  matches_winners = matches_list.select{|match| match.round > 0}
  matches_losers = matches_list.select{|match| match.round < 0}

  sets = []

  matches_list.each do |match|
    winner = tournament_participants.find{|x| x.last == match.winner_id}.first.tr(' ', '')
    loser = tournament_participants.find{|x| x.last == match.loser_id}.first.tr(' ', '')
    sets << [loser, winner]
  end

  # File for writing
  file = File.new('./Data/data_' + name + '.txt', "w+")

  # Writing
  file.puts name
  # file.puts tier
  file.puts tournament.participants.size
  file.write("\n")

  placings.each do |player|
    file.write(player.join(' ') + "\n")
  end

  file.write("\n")

  sets.each do |set|
    file.write(set.join(' ') + "\n")
  end

end
