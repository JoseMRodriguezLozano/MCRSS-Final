<template>
  <v-container>
    <v-row v-if="loading" justify="center">
      <v-progress-circular :active="loading" indeterminate :size="50" color="primary"></v-progress-circular>
    </v-row>
    <ErrorCard
      v-if="init_error && !loading"
      :in_color="uprm_color"
      :error_header="error_header"
      :error_message="error_message"
    />
    <v-card fixed v-if="!init_error && !loading">
      <v-toolbar color="green darken-1" dark flat>
        <v-spacer />
        <v-toolbar-title class="title">{{sportName}}</v-toolbar-title>
        <v-spacer />
      </v-toolbar>
      <v-container>
        <v-row align="center" justify="center">
          <BaseballScore
            :uprm_team="uprm_team_name"
            :opp_team="opponentName"
            :uprm_score="uprmScore"
            :opp_score="oppScore"
            :current_set="currentSet"
            :current_uprm_score="currentUPRMSet"
            :current_opp_score="currentOppSet"
            :event_id="event_id"
          />
        </v-row>
        <v-row>
          <v-col>
            <v-divider class="mx-4" horizontal></v-divider>
          </v-col>
        </v-row>
        <v-tabs align-with-title centered grow :color="uprm_color">
          <v-tabs-slider :color="uprm_color" />
          <v-tab>JUGADA A JUGADA</v-tab>

          <v-tab>ESTADÍSTICAS POR EQUIPO</v-tab>

          <v-tab>ESTADÍSTICAS POR ATLETAS</v-tab>

          <v-tab-item>
            <v-row justify="center">
              <v-card-title>Lista de Jugadas</v-card-title>
            </v-row>
            <v-container v-for="action in gameActions" :key="action.key + 500">
              <BaseballGameAction
                v-if="action.action_type === notification"
                align="center"
                justify="center"
                :action_type="action.action_type"
                :message="action.message"
                :athlete_number="action.athlete_number"
                :athlete_name="action.athlete_name"
                :athlete_img="action.athlete_img"
                in_color="gray"
                :id="action.key"
                :event_id="event_id"
                
              />
              <BaseballGameAction
                v-else-if="action.team === opp_keyword"
                align="center"
                justify="center"
                :action_type="action.action_type"
                :message="action.text"
                :athlete_number="findAthleteNumber(action.athlete_id, oppRoster)"
                :athlete_name="findAthleteName(action.athlete_id, 'opponent')"
                :athlete_id="action.athlete_id"
                :athlete_img="action.athlete_img"
                :in_color="oppColor"
                :id="action.key"
                :event_id="event_id"
                :uprmAthletes="uprmRoster"
                :oppAthletes="oppRoster"
                team="Oponente"
                
              />
              <BaseballGameAction
                v-else
                align="center"
                justify="center"
                :action_type="action.action_type"
                :message="action.text"
                :athlete_number="findAthleteNumber(action.athlete_id, uprmRoster)"
                :athlete_name="findAthleteName(action.athlete_id, 'uprm')"
                :athlete_img="findAthleteImg(action.athlete_id, uprmRoster)"
                :athlete_id="action.athlete_id"
                :in_color="uprm_color"
                :id="action.key"
                :event_id="event_id"
                :uprmAthletes="uprmRoster"
                :oppAthletes="oppRoster"
                team="UPRM"
                
              />
            </v-container>
          </v-tab-item>

          <v-tab-item>
            <v-spacer />
            <v-container>
              <v-row align="center" justify="center">
                <v-card-title>ANOTACIONES POR ENTRADA</v-card-title>
              </v-row>

              <v-row>
                <v-col>
                  <v-simple-table>
                    <template v-slot:default>
                      <thead>
                        <tr>
                          <th class="text-center">EQUIPO</th>
                          <th v-for="(n,index) in 9" class="text-center" :key="n + 500">ENTRADA {{index+1}}</th>
                          <th  class="text-center" v-if="currentSet > 9">ENTRADA 10 </th>
                          <th  class="text-center" v-if="currentSet > 10">ENTRADA 11 </th>
                          <th  class="text-center" v-if="currentSet > 11">ENTRADA 12 </th>
                          <th  class="text-center" v-if="currentSet > 12">ENTRADA 13 </th>
                          <th class="text-center">FINAL</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr :key="2525">
                          <td  class="text-center">{{ uprm_team_name }}</td>
                          <td v-for="(value,i) in 9" :key="uprmSets[value]" class="text-center">{{ uprmSets[i]}}</td>
                          <td  class="text-center" v-if="currentSet > 9">{{ uprmSets[9]}}</td>
                          <td  class="text-center" v-if="currentSet > 10">{{ uprmSets[10]}} </td>
                          <td  class="text-center" v-if="currentSet > 11">{{ uprmSets[11]}} </td>
                          <td  class="text-center" v-if="currentSet > 12">{{ uprmSets[12]}} </td>
                          <!-- <td class="text-center">{{}}</td> -->
                        </tr>
                        <tr :key="2526">
                          <td class="text-center">{{ opponentName }}</td>
                          <td v-for="(value,i) in 9" :key="oppSets[value]" class="text-center">{{ oppSets[i]}}</td>
                          <td  class="text-center" v-if="currentSet > 9">{{ oppSets[9]}}</td>
                          <td  class="text-center" v-if="currentSet > 10">{{ oppSets[10]}} </td>
                          <td  class="text-center" v-if="currentSet > 11">{{ oppSets[11]}} </td>
                          <td  class="text-center" v-if="currentSet > 12">{{ oppSets[12]}} </td>
                          <!-- <td  class="text-center">{{}}</td> -->
                        </tr>
                      </tbody>
                    </template>
                  </v-simple-table>
                </v-col>
              </v-row>

              <v-row>
                <v-col>
                  <v-divider class="mx-4" horizontal></v-divider>
                </v-col>
              </v-row>

              <v-tabs centered :color="uprm_color">
                <v-tabs-slider :color="uprm_color" />

                <v-tab>{{uprm_team_name}}</v-tab>
                <v-tab>{{opponentName}}</v-tab>
                <v-tab-item>
                  <BaseballStatistics :baseball_stats="uprmStatistics" />
                </v-tab-item>
                <v-tab-item>
                  <BaseballStatistics :baseball_stats="oppStatistics" />
                </v-tab-item>
              </v-tabs>
            </v-container>
          </v-tab-item>
          <v-tab-item>
            <v-spacer />
            <v-container>
              <v-tabs centered :color="uprm_color">
                <v-tabs-slider :color="uprm_color" />
                <v-tab>{{ uprm_team_name }}</v-tab>
                <v-tab>{{ opponentName }}</v-tab>
                <v-tab-item>
                  <v-data-table
                    dense
                    :headers="statistics_headers"
                    :items="uprmAthleteStatistics"
                    item-key="12344"
                    class="elevation-1"
                    :loading="loading"
                    loading-text="Cargando Estadísticas..."
                    no-data-text="No Se Encontraron Resultados"
                  />
                </v-tab-item>
                <v-tab-item>
                  <v-data-table
                    dense
                    :headers="statistics_headers"
                    :items="oppAthleteStatistics"
                    item-key="12345"
                    class="elevation-1"
                    :loading="loading"
                    loading-text="Cargando Estadísticas..."
                    no-data-text="No Se Encontraron Resultados"
                  />
                </v-tab-item>
              </v-tabs>
            </v-container>
          </v-tab-item>
        </v-tabs>
      </v-container>
    </v-card>
  </v-container>
</template>

<script>
import BaseballScore from "../../../../components/BaseballScore";
import BaseballStatistics from "../../../../components/BaseballStatistics";
import BaseballGameAction from "../../../../components/BaseballGameAction";
import ErrorCard from "../../../../components/PBP/ErrorCard";
import { mapGetters, mapActions } from "vuex";
export default {
  components: {
    BaseballScore,
    BaseballStatistics,
    BaseballGameAction,
    ErrorCard
  },
  data: () => ({
    loading: true,

    terms: false,

    invalid_event_dialog: false,
    no_pbp_dialog: false,
    invalid_sport_dialog: false,

    // Flag for controlling Error Card.
    init_error: false,
    // Strings for handling Error Card.
    error_header: "",
    error_message: "",

    // Header for statistics table (athletes).
    statistics_headers: [
      { text: "Número", value: "number", align: "center" },
      { text: "Nombre", value: "name", align: "center" },
      { text: "Hit", value: "hit", align: "center" },
      { text: "Al Bate", value: "atBat", align: "center" },
      { text: "Cuadrangular", value: "homerun", align: "center" },
      { text: "Carrera", value: "run", align: "center" },
      { text: "Carrera Empujada", value: "runBattedIn", align: "center" },
      { text: "Ponche", value: "strikeOut", align: "center" },
      { text: "Base Por Bola", value: "baseOnBall", align: "center" },
      { text: "Dejado En Base", value: "leftOnBase", align: "center" }
    ],

    event_id: Number,
    end_pbp_dialog: false,
    color_dialog: false,
    prev_color: null,
    button_loading: false,
    notification_dialog: false,
    notification_text: "",
    notification_rules: [
      v =>
        (!!v && v.length > 0 && v.length <= 100) ||
        "Las notificaciones deben tener entre 1 y 100 caracteres."
    ],
    uprm_color: "primary",
    notification: "Notification",
    uprm_team_name: "uprm",
    opp_keyword: "opponent",
  }),
  methods: {
   sendAdjust(team_name, adjust_no) {
      payload = {
        team: team_name,
        action_type: "ScoreAdjust",
        adjust: adjust_no
      };
      console.log(payload);
    },
    // Functions for init/detach callbacks for maintaining data models based on Firebase updates.
    ...mapActions({
      getEvent: "BaseballPBP/getEvent",
      getValidUPRMRoster: "BaseballPBP/getValidUPRMRoster",
      handleSetScores: "BaseballPBP/handleSetScores",
      handleCurrentSet: "BaseballPBP/handleCurrentSet",
      handleUPRMRoster: "BaseballPBP/handleUPRMRoster",
      handleOPPRoster: "BaseballPBP/handleOPPRoster",
      handleGameOver: "BaseballPBP/handleGameOver",
      handleOppColor: "BaseballPBP/handleOppColor",
      handleGameActions: "BaseballPBP/handleGameActions",
      detachSetScores: "BaseballPBP/detachSetScores",
      detachCurrentSet: "BaseballPBP/detachCurrentSet",
      detachUPRMRoster: "BaseballPBP/detachUPRMRoster",
      detachOPPRoster: "BaseballPBP/detachOPPRoster",
      detachGameOver: "BaseballPBP/detachGameOver",
      detachOppColor: "BaseballPBP/detachOppColor",
      detachGameActions: "BaseballPBP/detachGameActions",
      sendGameAction: "BaseballPBP/sendGameAction",
      endPBPSequence: "BaseballPBP/endPBPSequence",
      clearPBPState: "BaseballPBP/clearPBPState",
      updateOpponentColor: "BaseballPBP/updateOpponentColor"
    }),
    startEndPBPSequence() {
      // Set payload format.
      const payload = {
        event_id: this.event_id
      };
      // Send request for ending a PBP sequence.
      this.endPBPSequence(payload);
      this.end_pbp_dialog = false;
    },
    findAthleteName(athlete_id, team) {
      let athlete_index = -1;
      let roster = [];
      // Set the right roster.
      if (team === "uprm") {
        roster = this.uprmRoster;
      } else if (team === "opponent") {
        roster = this.oppRoster;
      }
      // Iterate through each element in roster.
      for (let index in roster) {
        if (roster[index].key == "athlete-" + athlete_id) {
          athlete_index = index;
          continue;
        }
      }
      if (athlete_index === -1) {
        return "Atleta Desconocido";
      }
      // If athlete is opponent, just return its name.
      if (team === "opponent") {
        return roster[athlete_index].name;
      }
      // Otherwise, build its name using the structure established by Odin.
      let athlete_name = roster[athlete_index].first_name;
      if (roster[athlete_index].middle_name !== "") {
        athlete_name += " " + roster[athlete_index].middle_name;
      }
      athlete_name += " " + roster[athlete_index].last_names;
      return athlete_name;
    },
    on_notification_pressed() {
      this.notification_dialog = true;
    },

    clear_end_pbp() {
      this.terms = false;
      this.end_pbp_dialog = false;
    },

    async send_notification() {
      if (this.$refs.create_form.validate()) {
        const payload = {
          event_id: this.event_id,
          data: {
            message: this.notification_text,
            action_type: "Notification"
          }
        };
        this.button_loading = true;
        if (await this.sendGameAction(payload)) {
          this.$refs.create_form.reset();
          this.notification_dialog = false;
        }
        this.button_loading = false;
      }
    },
    reset_notification() {
      this.notification_dialog = false;
      this.$refs.create_form.reset();
    },
    findAthleteNumber(athlete_id, roster) {
      let athlete_index = -1;
      for (let index in roster) {
        if (roster[index].key == "athlete-" + athlete_id) {
          athlete_index = index;
          continue;
        }
      }
      if (athlete_index === -1) {
        return "?";
      }
      return roster[athlete_index].number;
    },
    findAthleteImg(athlete_id, roster) {
      let athlete_index = -1;
      for (let index in roster) {
        if (roster[index].key == "athlete-" + athlete_id) {
          athlete_index = index;
          continue;
        }
      }
      if (athlete_index === -1) {
        return "";
      }
      return roster[athlete_index].profile_image_link;
    },
    // Set up variables for color update dialog.
    startChooseColor() {
      this.prev_color = this.color;
      this.color_dialog = true;
    },
    // Rollback to previous color in case cancel was pressed.
    cancelColorUpdate() {
      this.color = this.prev_color;
      this.color_dialog = false;
    },
    // Send request to Odin.
    async updateColor() {
      const payload = {
        event_id: this.event_id,
        color: this.color.hexa
      };
      this.button_loading = true;
      if (await this.updateOpponentColor(payload)) {
        this.color_dialog = false;
      }
      this.button_loading = false;
    }
  },
  computed: {
    // Functions for getting values in the data models.
    ...mapGetters({
      uprmSets: "BaseballPBP/uprmSets",
      oppSets: "BaseballPBP/oppSets",
      currentUPRMSet: "BaseballPBP/currentUPRMSet",
      currentOppSet: "BaseballPBP/currentOppSet",
      currentSet: "BaseballPBP/currentSet",
      uprmScore: "BaseballPBP/uprmScore",
      oppScore: "BaseballPBP/oppScore",
      uprmRoster: "BaseballPBP/uprmRoster",
      oppRoster: "BaseballPBP/oppRoster",
      gameOver: "BaseballPBP/gameOver",
      oppColor: "BaseballPBP/oppColor",
      gameActions: "BaseballPBP/gameActions",
      uprmStatistics: "BaseballPBP/uprmStatistics",
      oppStatistics: "BaseballPBP/oppStatistics",
      uprmAthleteStatistics: "BaseballPBP/uprmAthleteStatistics",
      oppAthleteStatistics: "BaseballPBP/oppAthleteStatistics",
      sportName: "BaseballPBP/sportName",
      hasPBP: "BaseballPBP/hasPBP",
      teamId: "BaseballPBP/teamId",
      validUPRMRoster: "BaseballPBP/validUPRMRoster",
      branch: "BaseballPBP/branch",
      opponentName: "BaseballPBP/opponentName"
    })
  },
  async beforeMount() {
    this.loading = true;
    this.init_error = false;
    let event_id = this.$route.params.id;

    // Validate ID has been passed.
    if (!!!event_id) {
      this.error_header = "Error de Argumento";
      this.error_message = "No se envió un identificador de evento.";
      this.init_error = true;
      this.loading = false;
      return;
    }

    // Validate that the passed id is an unsigned integer.
    if (!!!event_id.match(/^-{0,1}\d+$/) || parseInt(event_id) < 0) {
      this.error_header = "Argumento Inválido";
      this.error_message =
        "El identificador del evento debe ser un entero sin signo.";
      this.init_error = true;
      this.loading = false;
      return;
    }

    this.event_id = parseInt(this.$route.params.id);
    // Validate a valid event_id was provided.
    if (await this.getEvent(this.event_id)) {
      this.getValidUPRMRoster(this.teamId);
      this.handleSetScores(this.event_id);
      this.handleCurrentSet(this.event_id);
      this.handleUPRMRoster(this.event_id);
      this.handleOPPRoster(this.event_id);
      this.handleGameOver(this.event_id);
      this.handleOppColor(this.event_id);
      this.handleGameActions(this.event_id);
      if (this.branch === "Masculino") {
        this.uprm_team_name = "Tarzanes";
      } else {
        this.uprm_team_name = "Juanas";
      }
      this.invalid_event_dialog = false;
    } else {
      this.error_header = "Error en la solicitud";
      this.error_message =
        "Esto puede ser debido a problemas de conexión o debido a que el evento provisto no se encuentre en el sistema.";
      this.init_error = true;
      this.loading = false;
      return;
    }
    // Validate the event has PBP functionality.
    if (this.hasPBP === false) {
      this.error_header = "Evento Inválido";
      this.error_message = "Este evento no tiene funcionalidad Play-by-Play.";
      this.init_error = true;
      this.loading = false;
    }

    // Validate the PBP sequence corresponds to Baseball.
    if (this.sportName != "Beisbol" && this.sportName != "Softbol") {
      this.error_header = "Deporte Incorrecto";
      this.error_message =
        "Este deporte no está cubierto bajo la funcionalidad de Play-by-Play.";
      this.init_error = true;
      this.loading = false;
      return;
    }

    // All good at this point, so it is just needed to stop to loading animation.
    this.loading = false;
  },

  watch: {
    $route(to, from) {
      this.detachSetScores(this.event_id);
      this.detachCurrentSet(this.event_id);
      this.detachUPRMRoster(this.event_id);
      this.detachOPPRoster(this.event_id);
      this.detachGameOver(this.event_id);
      this.detachOppColor(this.event_id);
      this.detachGameActions(this.event_id);
      this.clearPBPState();
    }
  },
  beforeDestroy() {
    this.detachSetScores(this.event_id);
    this.detachCurrentSet(this.event_id);
    this.detachUPRMRoster(this.event_id);
    this.detachOPPRoster(this.event_id);
    this.detachGameOver(this.event_id);
    this.detachOppColor(this.event_id);
    this.detachGameActions(this.event_id);
    this.clearPBPState();
  }
};
</script>