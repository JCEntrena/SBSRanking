#!/usr/bin/env ruby
#encoding: utf-8

######################################
# Extracting data from Challonge.
######################################

require 'challonge-api'

# Set params.
Challonge::API.username = 'SmashBrosSpain'
Challonge::API.key = '' # KEEP PRIVATE

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
  # Participants.
  tournament_participants = []
  tournament.participants.each do |player|
    tournament_participants << [player.name.clone, player.id]
  end

  matches_list = tournament.matches.clone
  # Remove pools
  matches_list.select!{|match| match.group_id == nil}
  # Divide in winners and losers (not necessary)
  # Challonge has negative round number for sets in losers.
  matches_winners = matches_list.select{|match| match.round > 0}
  matches_losers = matches_list.select{|match| match.round < 0}

  sets = []

  matches_list.each do |match|
    winner = tournament_participants.find{|x| x.last == match.winner_id}.first.tr(' ', '')
    loser = tournament_participants.find{|x| x.last == match.loser_id}.first.tr(' ', '')
    sets << [loser, winner, 'c']
  end

  # File for writing
  file = File.new('./Data/data_' + name + '.txt', "w+")

  # Writing
  sets.each do |set|
    file.write(set.join(' ') + "\n")
  end

end
