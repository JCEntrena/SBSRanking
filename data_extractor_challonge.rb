#!/usr/bin/env ruby
#encoding: utf-8

######################################
# Extracting data from Challonge.
######################################

require 'challonge-api'

# Set params.
Challonge::API.username = ''
Challonge::API.key = '' # KEEP PRIVATE

# Season dates
@season_begin = Date.new(2018, 3, 3)
@season_end = Date.new(2018, 12, 31)

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
  # Divide in winners and losers
  # Challonge has negative round number for sets in losers.
  matches_winners = matches_list.select{|match| match.round > 0}
  matches_losers = matches_list.select{|match| match.round < 0}

  sets_winners = []
  sets_losers = []

  matches_winners.each do |match|
    winner = tournament_participants.find{|x| x.last == match.winner_id}.first.tr(' ', '')
    loser = tournament_participants.find{|x| x.last == match.loser_id}.first.tr(' ', '')
    sets_winners << [loser, winner, 'c', 'w']
  end

  matches_losers.each do |match|
    winner = tournament_participants.find{|x| x.last == match.winner_id}.first.tr(' ', '')
    loser = tournament_participants.find{|x| x.last == match.loser_id}.first.tr(' ', '')
    sets_losers << [loser, winner, 'c', 'l']
  end

  # File for writing
  file = File.new('./Data/data_' + name + '.txt', "w+")
  # Writing winners
  sets_winners.each do |set|
    file.write(set.join(' ') + "\n")
  end
  # Writing losers
  sets_losers.each do |set|
    file.write(set.join(' ') + "\n")
  end

end
