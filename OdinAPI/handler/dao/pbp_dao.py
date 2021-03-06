from .config.fb_config import serv_path, rtdb_config
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from time import time


class PBPDao:
    '''
    PBPDao - This class implements a Data Access Object pattern to provide 
             Odin API interaction to information about sport play-by-play 
             sequences stored in the non-relational database.
    @author Pedro Luis Rivera Gomez
    '''

    # Initialize Firebase Admin SDK and set Realtime Database instance.
    def __init__(self):
        if not firebase_admin._apps:
            firebase_admin.initialize_app(
                credentials.Certificate(serv_path), rtdb_config)
        self._rtdb = db
        # TODO -> Move this into the a separate file such as fb_config.py.
        self._db_keywords = {
            "root": "/v1/",
            "meta": "/game-metadata",
            "meta-key": "game-metadata",
            "uprm-roster": "/uprm-roster",
            "opp-roster": "/opponent-roster",
            "set": "/game-metadata/current-set",
            "score": "/score",
            "actions": "/game-actions",
            "score-key": "score",
            "over": "/game-over/answer",
            "answer": "/answer",
            "color": "/opp-color",
            "athlete_prefix": "athlete-"
        }

    def create_pbp_seq(self, event_id, game_metadata, score_val):
        """
        Initialize a PBP sequence for a valid sport event.
        This function creates a PBP sequence initializing its metadata and scoring system.

        Args
            event_id: integer corresponding to an event id.
            game_metadata: JSON object containing general information about a PBP sequence depending on the sport.
            score_val: JSON object containing the initial scores per period of a PBP sequence depending on the sport.

        Returns:
            void
        """

        event_node = {
            self._db_keywords["meta-key"]: game_metadata,
            self._db_keywords["score-key"]: score_val
        }

        path = self._db_keywords["root"] + str(int(event_id))
        self._rtdb.reference(path).set(event_node)

    def remove_pbp_seq(self, event_id):
        """
        Remove a PBP sequence from the non-relational database.
        This function deletes a PBP sequence's node from the non-relational database.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            void
        """

        path = self._db_keywords["root"] + str(int(event_id))
        return self._rtdb.reference(path).delete()

    def set_uprm_athlete(self, event_id, athlete_entry):
        """
        Add an athlete to UPRM roster or updates its value if exists in the system.
        This function adds an athlete to UPRM roster given it's PBP sequence's event_id.
        If the athlete exists, it updates its information.

        Args
            event_id: integer corresponding to an event id.
            athlete_entry: JSON corresponding to the athlete entry to be set in the RTDB.

        Returns:
            void
        """

        path = self._db_keywords["root"] + \
            str(int(event_id)) + \
            self._db_keywords["uprm-roster"] + \
            "/" + self._db_keywords["athlete_prefix"] + \
            str(int(athlete_entry["athlete_id"]))
        self._rtdb.reference(path).set(athlete_entry)


    def set_opponent_athlete(self, event_id, athlete_entry):
        """
        Add an athlete to opponent roster or updates its value if exists in the system.
        This function adds an athlete to opponent roster given it's PBP sequence's event_id.
        If the athlete exists, it updates its information.

        Args
            event_id: integer corresponding to an event id.
            athlete_entry: JSON corresponding to the athlete entry to be set in the RTDB.

        Returns:
            void
        """

        path = self._db_keywords["root"] + \
            str(int(event_id)) + \
            self._db_keywords["opp-roster"] + \
            "/" + self._db_keywords["athlete_prefix"] + \
            str(int(athlete_entry["number"]))
        self._rtdb.reference(path).set(athlete_entry)

    def remove_uprm_athlete(self, event_id, athlete_id):
        """
        Removes a UPRM athlete from the PBP sequence.
        This function deletes a particular UPRM athlete from PBP sequence.

        Args
            event_id: integer corresponding to an event id.
            athlete_id: integer corresponding to the athlete to remove.

        Returns:
            void
        """

        path = self._db_keywords["root"] + \
            str(int(event_id)) + \
            self._db_keywords["uprm-roster"] + \
            "/" + self._db_keywords["athlete_prefix"] + \
            str(int(athlete_id))
        self._rtdb.reference(path).delete()

    def remove_opponent_athlete(self, event_id, athlete_id):
        """
        Removes an opponent athlete from the PBP sequence.
        This function deletes a particular opponent athlete from PBP sequence.

        Args
            event_id: integer corresponding to an event id.
            athlete_id: integer corresponding to the athlete to remove.

        Returns:
            void
        """

        path = self._db_keywords["root"] + \
            str(int(event_id)) + \
            self._db_keywords["opp-roster"] + \
            "/" + self._db_keywords["athlete_prefix"] + \
            str(int(athlete_id))
        self._rtdb.reference(path).delete()

    def get_uprm_roster(self, event_id):
        """
        Get UPRM roster of an existing PBP sequence.
        This function returns a dictionary with the UPRM roster given the event_id of a PBP sequence.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            dictionary containing UPRM athlete entries for the PBP sequence.
        """

        path = self._db_keywords["root"] + \
            str(int(event_id)) + self._db_keywords["uprm-roster"]
        return self._rtdb.reference(path).get()

    def get_opponent_roster(self, event_id):
        """
        Get opponent roster of an existing PBP sequence.
        This function returns a dictionary with the opponent roster given the event_id of a PBP sequence.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            dictionary containing opponent athlete entries for the PBP sequence.
        """

        path = self._db_keywords["root"] + \
            str(int(event_id)) + self._db_keywords["opp-roster"]
        return self._rtdb.reference(path).get()

    def pbp_exists(self, event_id):
        """
        Determines if a PBP sequence exists.
        This function determines whether a PBP sequence exists in the non-relational database.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            Boolean that determines if the PBP sequence exists.
        """

        return self.get_pbp_meta(event_id) != None

    def get_pbp_meta(self, event_id):
        """
        Get PBP sequence metadata.
        This function fetches a PBP sequence metadata from the non-relational database.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            dictionary that contains the pbp information (metadata: sport, game-ended).
        """

        path = self._db_keywords["root"] + \
            str(int(event_id)) + self._db_keywords["meta"]
        return self._rtdb.reference(path).get()

    def set_current_set_baseball(self, event_id, new_set,otuprm,otopp):
        """
        Updates the current set or period for a PBP sequence.
        This function sets the current set or period value of a PBP sequence given its id.

        Args
            event_id: integer corresponding to an event id.
            new_set: integer corresponding to the new set or period value.

        Returns:
            void
        """

        path = self._db_keywords["root"] + \
               str(int(event_id)) + self._db_keywords["set"]
        self._rtdb.reference(path).set(int(new_set))

        if new_set > 9:
            temp = {
                otuprm: 0,
                otopp: 0
            }
            path = self._db_keywords["root"] + str(int(event_id)) + '/' + self._db_keywords["score-key"]
            self._rtdb.reference(path).update(temp)


    def set_current_set_basketball(self, event_id, new_set,otuprm,otopp):
        """
        Updates the current set or period for a PBP sequence.
        This function sets the current set or period value of a PBP sequence given its id.

        Args
            event_id: integer corresponding to an event id.
            new_set: integer corresponding to the new set or period value.

        Returns:
            void
        """

        path = self._db_keywords["root"] + \
            str(int(event_id)) + self._db_keywords["set"]
        self._rtdb.reference(path).set(int(new_set))

        if new_set > 4:
            temp= {
                otuprm:0,
                otopp:0

            }
            path = self._db_keywords["root"] + str(int(event_id)) + '/' + self._db_keywords["score-key"]
            self._rtdb.reference(path).update(temp)




    def set_current_set(self, event_id,new_set):
        """
        Updates the current set or period for a PBP sequence.
        This function sets the current set or period value of a PBP sequence given its id.

        Args
            event_id: integer corresponding to an event id.
            new_set: integer corresponding to the new set or period value.

        Returns:
            void
        """

        path = self._db_keywords["root"] + \
            str(int(event_id)) + self._db_keywords["set"]
        self._rtdb.reference(path).set(int(new_set))

    def get_current_set(self, event_id):
        """
        Gets the current set or period for a PBP sequence.
        This function gets the current set or period value of a PBP sequence given its id.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            integer denoting the current set or period of a PBP sequence.
        """

        path = self._db_keywords["root"] + \
            str(int(event_id)) + self._db_keywords["set"]

        return self._rtdb.reference(path).get()

    def set_score_by_set(self, event_id, set_path, score):
        """
        Sets the score for a set or period for a PBP sequence.
        This function updates the score for a given set or period value of a PBP sequence.

        Args
            event_id: integer corresponding to an event id.
            set_path: path that denotes the set (denoted by team and sport, i.e. set5-uprm for a volleyball game).
            score: integer value to be set as new score.

        Returns:
            void
        """
        self._rtdb.reference(
            self._db_keywords["root"] + str(int(event_id)) + self._db_keywords["score"] + set_path).set(score)

    def get_score_by_set(self, event_id, set_path):
        """
        Gets the score for a set or period for a PBP sequence.
        This function retrieves and returns the score for a given set or period value of a PBP sequence.

        Args
            event_id: integer corresponding to an event id.
            set_path: path that denotes the set (denoted by team and sport, i.e. set5-uprm for a volleyball game).

        Returns:
            integer that denotes the score for a given set or game period.
        """

        return self._rtdb.reference(self._db_keywords["root"] + str(int(event_id)) + self._db_keywords["score"] + set_path).get()

    def adjust_score_by_set(self, event_id, set_path, adjust):
        """
        Adjusts the score for a set or period for a PBP sequence.
        This function updates the score for a given set or period value of a PBP sequence.

        Args
            event_id: integer corresponding to an event id.
            set_path: path that denotes the set (denoted by team and sport, i.e. set5-uprm for a volleyball game).
            adjust: increment amount to be added to the current score.

        Returns:
            void
        """

        current_score = int(self.get_score_by_set(event_id, set_path))
        if current_score + int(adjust) < 0:
            raise Exception("PBPDao.adjust_score_by_set: Invalid score state.")
        self.set_score_by_set(event_id, set_path, current_score + int(adjust))

    def adjust_score_by_differential(self, event_id, path_dec, path_inc, difference):
        """
        Adjusts the score for a set or period for a PBP sequence for both teams.
        This function updates the score for a given set or period value of a PBP 
        sequence for both teams, increasing one and decreasing the other.

        Args
            event_id: integer corresponding to an event id.
            path_dec: path that denotes the set to be decreased (denoted by team and sport, i.e. set5-uprm for a volleyball game).
            path_inc: path that denotes the set to be incremented (denoted by team and sport, i.e. set5-uprm for a volleyball game).
            difference: amount to be added and subtracted to the current score at path_inc and path_dec respectively. 

        Returns:
            void
        """

        dec_score = int(self.get_score_by_set(event_id, path_dec))
        inc_score = int(self.get_score_by_set(event_id, path_inc))

        if dec_score - int(difference) < 0 or inc_score + int(difference) < 0:
            raise Exception("PBPDao.adjust_score_by_set: Invalid score state.")

        update = {
            (event_id + path_dec): dec_score - difference,
            (event_id + path_inc): inc_score + difference,
        }
        path = self._db_keywords["root"] + \
            str(int(event_id)) + self._db_keywords["score"]
        self._rtdb.reference(path).update(update)

    def adjust_score_by_play_edit(self, event_id, path_dec, path_inc, difference, action_id, new_action):
        """
        Adjusts the score for a set or period for a PBP sequence for both teams and adds a play.
        This function updates the score of two teams for a given set or period value of a PBP 
        sequence for both teams, increasing one and decreasing the other. Also inserts the game action.

        Args
            event_id: integer corresponding to an event id.
            path_dec: path that denotes the set to be decreased (denoted by team and sport, i.e. set5-uprm for a volleyball game).
            path_inc: path that denotes the set to be incremented (denoted by team and sport, i.e. set5-uprm for a volleyball game).
            difference: amount to be added and subtracted to the current score at path_inc and path_dec respectively. 
            action_id: integer that denotes the action id.
            new_action: JSON object that denotes the action to be inserted.

        Returns:
            void
        """
        event_id = str(int(event_id))
        dec_score = int(self.get_score_by_set(event_id, path_dec))
        inc_score = int(self.get_score_by_set(event_id, path_inc))
        action_path = self._db_keywords["root"] + \
            event_id + \
            self._db_keywords["actions"] + "/" + str(int(action_id))

        if dec_score + int(difference) < 0 or inc_score + int(difference) < 0:
            raise Exception("PBPDao.adjust_score_by_set: Invalid score state.")

        update = {
            (self._db_keywords["root"] + event_id + self._db_keywords["score"] + path_dec): dec_score - difference,
            (self._db_keywords["root"] + event_id + self._db_keywords["score"] + path_inc): inc_score + difference,
            action_path: new_action
        }
        self._rtdb.reference().update(update)

    def adjust_score_by_play_edit_inc(self, event_id, path_inc, increment, action_id, new_action):
        """
        Adjusts the score for a set or period for a PBP sequence for a team and adds a play.
        This function updates the score of two teams for a given set or period value of a PBP 
        sequence for one team. Also inserts the game action.

        Args
            event_id: integer corresponding to an event id.
            path_inc: path that denotes the set to be incremented (denoted by team and sport, i.e. set5-uprm for a volleyball game).
            increment: amount to be added to the current score at path_inc. 
            action_id: integer that denotes the action id.
            new_action: JSON object that denotes the action to be inserted.

        Returns:
            void
        """

        inc_score = int(self.get_score_by_set(event_id, path_inc))
        action_path = self._db_keywords["root"] + \
            str(int(event_id)) + \
            self._db_keywords["actions"] + "/" + str(int(action_id))

        path_score = self._db_keywords["root"] + \
            str(int(event_id)) + \
            self._db_keywords["score"] + "/" + str(path_inc)

        if inc_score + int(increment) < 0:
            raise Exception("PBPDao.adjust_score_by_set: Invalid score state.")

        update = {
            path_score: inc_score + increment,
            action_path: new_action
        }
        self._rtdb.reference().update(update)

    def get_opponent_color(self, event_id):
        """
        Gets the opponent color.
        This function retrieves the opponent color of a particular PBP sequence int he NoSQL database.

        Args
            event_id: integer corresponding to an event id.

        Returns
            color: string denoting the opponent team color.
        """
        return self._rtdb.reference(self._db_keywords["root"] +
                                    str(int(event_id)) +
                                    self._db_keywords["meta"] + self._db_keywords["color"]).get()

    def set_opponent_color(self, event_id, color):
        """
        Sets the opponent color.
        This function sets the opponent color of a particular PBP sequence in the NoSQL database.

        Args
            event_id: integer corresponding to an event id.
            color: string corresponding to a hex-formatted color.

        Returns:
            void
        """

        path = self._db_keywords["root"] + \
            str(int(event_id)) + \
            self._db_keywords["meta"] + self._db_keywords["color"]
        self._rtdb.reference(path).set(color)

    def pbp_game_action_exists(self, event_id, action_id):
        """
        Determines if a PBP action exists.
        This function determines whether a particular game action exists as part of a PBP sequence.

        Args
            event_id: integer corresponding to an event id.
            action_id: string corresponding to the game action to check.

        Returns:
            Boolean that determines if the game action exists.
        """

        return self.get_pbp_action(event_id, action_id) != None

    def get_pbp_action(self, event_id, action_id):
        """
        Find a PBP sequence action..
        This function returns a PBP action given its event and action id.

        Args
            event_id: integer corresponding to an event id.
            action_id: string corresponding to the game action to get.

        Returns:
            Boolean that determines if the game action exists.
        """

        path = self._db_keywords["root"] + \
            str(int(event_id)) + \
            self._db_keywords["actions"] + "/" + str(int(action_id))

        return self._rtdb.reference(path).get()

    def add_pbp_game_action(self, event_id, action_content):
        """
        Adds a game action from PBP sequence.
        This function inserts a particular game action into PBP sequence.

        Args
            event_id: integer corresponding to an event id.
            action_content: JSON object corresponding to the new action content.

        Returns:
            ID corresponding to the newly inserted game action.
        """

        path = self._db_keywords["root"] + \
            str(int(event_id)) + \
            self._db_keywords["actions"] + "/" + str(int(time()))

        return self._rtdb.reference(path).set(action_content)

    def add_scoring_pbp_game_action(self, event_id, action_content, path_score, difference):
        """
        Adds a game action from PBP sequence, also edits the score.
        This function inserts a particular game action into PBP sequence.

        Args
            event_id: integer corresponding to an event id.
            action_content: JSON object corresponding to the new action content.

        Returns:
            ID corresponding to the newly inserted game action.
        """

        path_actions = self._db_keywords["root"] + \
            str(int(event_id)) + \
            self._db_keywords["actions"] + "/" + str(int(time()))
        current_score = int(self.get_score_by_set(event_id, path_score))

        if current_score + int(difference) < 0:
            raise Exception("PBPDao.adjust_score_by_set: Invalid score state.")

        update_path_score = self._db_keywords["root"] + \
            str(int(event_id)) + self._db_keywords["score"] + path_score

        update = {
            path_actions: action_content,
            update_path_score: current_score + difference,
        }

        return self._rtdb.reference().update(update)

    def edit_pbp_game_action(self, event_id, action_id, action_content):
        """
        Edits a game action from PBP sequence.
        This function updates a particular game action from PBP sequence.

        Args
            event_id: integer corresponding to an event id.
            action_id: string corresponding to the game action to edit.
            action_content: JSON object corresponding to the new action content.

        Returns:
            void
        """

        path = self._db_keywords["root"] + \
            str(int(event_id)) + \
            self._db_keywords["actions"] + "/" + str(int(action_id))
        return self._rtdb.reference(path).set(action_content)

    def edit_pbp_time_game_action(self, event_id, action_id, time):
        """
        Edits a game action from PBP sequence.
        This function updates a particular game action from PBP sequence.

        Args
            event_id: integer corresponding to an event id.
            action_id: string corresponding to the game action to edit.
            action_content: JSON object corresponding to the new action content.

        Returns:
            void
        """
        timepath="/time"
        path = self._db_keywords["root"] + \
            str(int(event_id)) + \
            self._db_keywords["actions"] + "/" + str(int(action_id) )+ timepath
        return self._rtdb.reference(path).set(time)

    def remove_pbp_game_action(self, event_id, action_id):
        """
        Removes a game action from PBP sequence.
        This function deletes a particular game action from PBP sequence.

        Args
            event_id: integer corresponding to an event id.
            action_id: string corresponding to the game action to remove.

        Returns:
            void
        """

        path = self._db_keywords["root"] + str(int(event_id)) + \
            self._db_keywords["actions"] + "/" + str(int(action_id))

        self._rtdb.reference(path).delete()

    def is_game_over(self, event_id):
        """
        Determines if a particular game is over.
        This function returns the game-ended status of a PBP sequence (Boolean).

        Args
            event_id: integer corresponding to an event id.

        Returns:
            Boolean result that determines if the game is over or not.
        """

        path = self._db_keywords["root"] + str(int(event_id)) + \
            self._db_keywords["meta"] + \
            self._db_keywords["over"]

        return self._rtdb.reference(path).get() == "Yes"

    def set_pbp_game_over(self, event_id):
        """
        Marks a PBP sequence state as over.
        This function modifies the game-ended status of a PBP sequence to true.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            void
        """

        path = self._db_keywords["root"] + str(int(event_id)) + \
            self._db_keywords["meta"] + self._db_keywords["over"]
        self._rtdb.reference(path).set("Yes")


# if __name__ == '__main__':

    # # Initialize a Play-by-Play DAO for quick testing purposes.
    # pbp_dao = PBPDao()
    # print(pbp_dao._rtdb.reference("v1").get())
    # print(pbp_dao.pbp_exists("123412341234"))
    # pbp_dao.adjust_score_by_differential("123412341234", "/a", "/b", 10)
