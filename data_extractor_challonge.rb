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
@season_end = Date.new(2018, 8, 17)

@TIER_A_FACTOR = 1.1923064
@TIER_B_FACTOR = 1.588010334
@TIER_C_FACTOR = 3.535334183

def remove_invalid_chars(str)
  str = str.split("/").last.split("|").last
  str.downcase.gsub(/[^a-zA-Z0-9áéíóúñ]+/, '')
end

def get_points(placing, points, tier)
  ## Correction factor.
  factor = 1
  max_position_points = 49
  case tier
  when "A"
    factor = @TIER_A_FACTOR
    max_position_points = 25
  when "B"
    factor = @TIER_B_FACTOR
    max_position_points = 13
  when "C"
    factor = @TIER_C_FACTOR
    max_position_points = 7
  end

  if placing > max_position_points
    return 0
  end

  return (points / (1000.0 * placing * factor))

end


# Get tournament data
tournament_data = []
File.foreach("torneoschallonge.txt") do |line|
  temp_tournament = line.split(' ')
  temp_dict = {}
  temp_dict["name"] = temp_tournament[0]
  temp_dict["tier"] = temp_tournament[1]
  temp_dict["points"] = temp_tournament[2]
  tournament_data << temp_dict
end

# Get tournaments.
tournaments = Challonge::Tournament.find(:all)
# Remove tournaments of other seasons.
tournaments.select!{|x| x.completed_at != nil}
tournaments.select!{|x| Date.parse(x.completed_at) <= @season_end and Date.parse(x.completed_at) >= @season_begin}

tournaments.each do |tournament|
  # Get name (for data files names)
  name = tournament.name.clone
  name.tr!(' ', '')
  # Data from file
  puts name
  data = tournament_data.find{|x| x["name"] == name}
  if data == nil
    next
  end
  tier = data["tier"]
  points = data["points"].to_f
  # Participants.

  placings = []
  tournament_participants = []

  tournament.participants.each do |player|
    placings << [remove_invalid_chars(player.name.clone), get_points(player.final_rank, points, tier)]
    placings.sort!{|a, b| b[1] <=> a[1]}
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
  # Changes id into name
  matches_list.each do |match|
    winner = tournament_participants.find{|x| x.last == match.winner_id}.first
    loser = tournament_participants.find{|x| x.last == match.loser_id}.first
    sets << [remove_invalid_chars(winner), remove_invalid_chars(loser)]
  end

  # File for writing
  file = File.new('./Data2/challonge_data_' + name + '.txt', "w+")

  # Writing
  file.puts name
  file.puts tier
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
