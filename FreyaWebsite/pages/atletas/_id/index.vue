<template>
	<v-card>
		<v-toolbar
				color="green darken-1"
				dark
				flat
		>
			<v-spacer />
			<v-toolbar-title> Perfil de Atleta </v-toolbar-title>
			<v-progress-linear
				:active="!ready"
				indeterminate
				absolute
				bottom
				color = "white"
			></v-progress-linear>
			<v-spacer />
		</v-toolbar>
		<v-container v-if="formated() && ready && athleteExists">
			<v-tabs
					centered
			>
				<v-tabs-slider/>
				<v-tab>
						Información				
				</v-tab>

				<v-tab>
						Estadísticas por Temporada						
				</v-tab>

				<v-tab-item>
				
						<v-card outlined>								
							
								
								<v-row class="ma-0 pa-0">
									<v-col md="auto">
										
										<v-avatar
												class="profile"
												color="grey"
												size="200"																																														
										>
											<v-icon v-if="profile_image_link == ''">mdi-account </v-icon>
											<v-img v-else :src="profile_image_link"></v-img>																											
										</v-avatar> 																					
									</v-col>

									<v-col md="auto">
										<v-card-text>
										<h1>{{first_name}} {{middle_name}} {{last_names}} </h1>
										<span class="text" style="font-size:20px"><b>Fecha de Nacimiento:</b> {{date_of_birth}} </span>
										<v-spacer/>	
										<span class="text" style="font-size:20px"><b>Estatura:</b> {{height_feet}}' {{height_inches}}" </span>
										<v-spacer/>	
										<span class="text" style="font-size:20px"><b>Programa de Estudio:</b> {{study_program}} </span>	
										<v-spacer/>
										<span class="text" style="font-size:20px"><b>Año de Estudio:</b> {{years_of_study}}</span>
										<v-spacer/>
										<span class="text" style="font-size:20px"><b>Escuela de Precedencia:</b> {{school_of_precedence}} </span>
										</v-card-text>							
									</v-col>

									<v-col md="auto">
										<v-card-text>
										<v-spacer/>
										<span class="text" style="font-size:20px"><b>Deporte:</b> {{sport}}</span>
										<v-spacer/>	
										<span class="text" style="font-size:20px"><b>Rama:</b> {{branch}}</span>
										<v-spacer/>									
										<span class="text" style="font-size:20px"><b>Años de Participación:</b> {{years_of_participation}}</span>
										<v-spacer/>	
										<span class="text" style="font-size:20px"><b>Número:</b> {{number}} </span>										
										</v-card-text>
									</v-col>
							
								
									<v-col v-if="athlete_positions !=''" md="auto">
											<v-card-text>
												<h2> Posiciones: </h2>										
												<div v-for="position in athlete_positions" v-bind:key="position.id">
													<span class="text" style="font-size:20px">{{position}}</span>
												</div>
											</v-card-text>
									</v-col>

									<v-col v-if="athlete_categories !=''" md="auto">
											<v-card-text>
												<h2> 	Categorías: </h2>										
												<div v-for="category in athlete_categories" v-bind:key="category.id">
													<span class="text" style="font-size:20px">{{category}}</span>
												</div>
											</v-card-text>
									</v-col>
									<v-col md="auto">
										<v-card-text>
											<h2> Biografía: </h2>
											<p style="font-size:20px">
												{{short_bio}}
											</p>
										</v-card-text>
										<v-row>
										<ShareNetwork
										class="ml-9"
										network="twitter"
										:url= this.url+this.id
										:title=" this.first_name+' '+this.last_names"
										:media= this.profile_image_link
										>
										<i class="fab fah fa-lg fa-twitter"></i>
										<v-tooltip bottom>
										<template v-slot:activator="{ on }">
											<v-btn color="#00acee" fab small dark target="_blank" v-on="on">
											<v-icon>mdi-twitter</v-icon>
											</v-btn>
										</template>
										<span>Compartelo en Twitter</span>
										</v-tooltip>
										
									</ShareNetwork>
									<ShareNetwork
										class="ml-7"
										network="facebook"
										:url= this.url+this.id
										:title=" this.first_name+' '+this.last_names"
										:media= this.profile_image_link
										>
										<i ></i>
										<v-tooltip bottom>
										<template v-slot:activator="{ on }">
											<v-btn color="#3b5998" fab small dark  target="_blank" v-on="on">
											<v-icon>mdi-facebook</v-icon>
											</v-btn>
										</template>
										<span>Compartelo en Facebook</span>
										</v-tooltip>

									    </ShareNetwork>
										</v-row>
									</v-col>
									
									
								
								</v-row>
						
						</v-card>
						
				</v-tab-item>
				<v-tab-item>
						
						<v-card flat>
							<v-row>
								<v-col md=3>
									<v-autocomplete
										v-model="season"
										:items="seasons"
										label ="Seleccione Temporada"	
										v-on:change="getSeasonData()"							
									></v-autocomplete>
								</v-col>							
							</v-row>

					
							<v-row v-if="aggregate_statistics_per_season.length>0">
								<v-col>
									<v-card-text>
									 <h2> Estadísticas de la Temporada {{season}}: </h2>
									</v-card-text>
									<v-data-table 
										dense 
										:headers="headers_" 
										:items="aggregate_statistics_per_season" 										
										class="elevation-1"
										loading="fetchingAthleteStats"																					
										loading-text="Recolectando Data...Por favor espere"
										no-data-text="No hay estadísticas para esta temporada."										
									>		
									</v-data-table>
								</v-col>
							</v-row>

							<v-row v-if="aggregate_statistics_per_season.length == 0 && season=='' ">
								<v-col>
									<v-card-text>
										<h2> Tiene que seleccionar una temporada </h2>
									</v-card-text>
								</v-col>
							</v-row>
							<v-row v-if="aggregate_statistics_per_season.length == 0 && fetchedData && !(season=='')">
								<v-col>
									<v-card-text>
										<h2> No hay estadísticas para la temporada: {{season}}  </h2>
									</v-card-text>
								</v-col>
							</v-row>

							<v-row justify="center" v-if="fetchingAthleteStats">
								<v-col>
									<div class="text-center">
										<h2> Buscando estadísticas</h2>
										<v-progress-circular
											indeterminate
											color="primary"
										></v-progress-circular>
									</div>
								</v-col>
							</v-row>

							<v-row v-if="statistics_per_season.length>0">
								<v-col>
									<v-card-text>
									 <h2> Estadísticas por Evento de la Temporada {{season}}: </h2>
									</v-card-text>
									<v-data-table 
										dense 
										:headers="headers" 
										:items="statistics_per_season"										 
										class="elevation-1"
										loading="fetchingAthleteStats"	
										no-data-text="No hay estadísticas para esta temporada."															
										loading-text="Recolectando Data...Por favor espere"																			
									>		
									</v-data-table>
								</v-col>
							</v-row>
							
							<v-row v-if="statistics_per_season.length == 0 && fetchedData && !(season=='')">
								<v-col>
									<v-card-text>
										<h2> No hay estadísticas por evento para la temporada: {{season}}  </h2>
									</v-card-text>
								</v-col>
							</v-row>

						</v-card>
				
				</v-tab-item>
			
			</v-tabs>
		</v-container> 
		<v-container v-if="!athleteExists">
				<v-row justify="center">
					<v-col>
						<h1> No existe este atleta </h1>
					</v-col>
				</v-row>
		</v-container>       
			
	</v-card>
</template>

<script>
import { mapActions, mapGetters} from "vuex"


export default {

    data: () =>({    
     
      ready: false,
      first_name: '',
      middle_name: '',
			last_names:'',
			date_of_birth:'',
      short_bio:'',
      height_feet:'',
			height_inches:'',
			athleteExists:true,

      study_program:'', 
      date_of_birth:'',
			school_of_precedence:'',
			years_of_participation:'',
			years_of_study:'',
      athlete_positions:'',
      athlete_categories:'',      
      number:'',
      profile_image_link:'',
      sport:'',     
			branch:'',
			sport_id:'', 
			fetchingAthleteStats:false,
			fetchedData:false,

			season:'',
			seasons:[],
			headers:[],
			headers_:[],
			statistics_per_season:[],
			aggregate_statistics_per_season:[],
			url:'https://huella-deportiva-web.ue.r.appspot.com/atletas/',
			id:'',
    }),//end of data()
		
		methods: {
			...mapActions({
				getAthleteByID:"athletes/getAthleteByID",
				getAthleteSeasonStats:"athletes/getAthleteSeasonStats",
				getAthleteAggregateSeasonStats:"athletes/getAthleteAggregateSeasonStats"
			}),

			/**
			 * Returns true if the contents of
			 * the athlete view page have been formated
			 * false otherwise.If the contents are not
			 * formated it then proceeds to format the
			 * contents. 
			 */
			async formated(){
				
				if(this.ready){
					return true
				}
				else{

					const response = await this.getAthleteByID(this.$route.params.id)
					if(response == 'error'){
						this.athleteExists = false
						this.ready = true
						return true
					}
					this.id = this.athlete.id
					this.first_name = this.athlete.fName
					this.last_names = this.athlete.lName	
					if(this.athlete.mName)
						this.middle_name = this.athlete.mName

					this.sport = this.athlete.sportName
					this.branch = this.athlete.sportBranch
					this.sport_id = this.athlete.sport_id

					if(this.athlete.bio)
						this.short_bio = this.athlete.bio

					if(this.athlete.number !== null && this.athlete.number !== '')
						this.number = this.athlete.number

					if(this.athlete.height)
					{
						this.height_feet = Math.floor(this.athlete.height/12)
						this.height_inches = this.athlete.height%12
					}

					if(this.athlete.profilePicLink)
						this.profile_image_link = this.athlete.profilePicLink
					

					if(this.athlete.school)
						this.school_of_precedence = this.athlete.school

					if(this.athlete.sProgram)
						this.study_program = this.athlete.sProgram
					
					if(this.athlete.yearOfStudy)
						this.years_of_study = this.athlete.yearOfStudy
					
					if(this.athlete.yearsOfParticipation)
						this.years_of_participation = this.athlete.yearsOfParticipation						
					
					if(this.athlete.dBirth)
						this.date_of_birth= new Date(Date.parse(this.athlete.dBirth)).toISOString().substr(0,10)
					
					if(this.athlete.athlete_positions)
					{
						this.athlete_positions = []
						const entries = Object.entries(this.athlete.athlete_positions)
						for(const [name, value] of entries){
							if(!value){
								this.athlete_positions.push(name)
							}
						}
					}
					if(this.athlete.athlete_categories)
					{
						this.athlete_categories = []
						const entries = Object.entries(this.athlete.athlete_categories)
						for(const [name, value] of entries){
							if(!value){
								this.athlete_categories.push(name)
							}
						}
					}	
					
					this.buildSeasonList()
					this.ready = true
					return true
				}
			
				

			},

			/**
			 * Build season year list for selection
			 */
			buildSeasonList(){
        let yearToAdd = 2020
        let currentYear = new Date(Date.now()).getFullYear()        
        
        while(yearToAdd <= currentYear)
        {
            this.seasons.push(yearToAdd++)
        }
      },
		
			/**
			 * Returns the date of the event given
			 * formated so that it can be used in the 
			 * stats table.
			 * @param event_date Date of the event
			 */
			formatedDate(event_date){
				
				const date = new Date(event_date).toISOString().substring(0,10)

				return date

			},
			
			/**
			 * Fetches and prepares the season
			 * data for the athlete statistics
			 * viewer tab.
			 */
			async getSeasonData(){
				
				if(this.season !=='')
				{
					this.statistics_per_season = []
					this.aggregate_statistics_per_season = []
					this.fetchingAthleteStats = true
					this.fetchedData =false
					let sport_name = ''
					
					//This if and else if statements determine the sport
					//name to be used for the route to use in the actions
					if(this.sport.localeCompare("Baloncesto") == 0){
						sport_name = "basketball"
					}
					else if(this.sport.localeCompare("Voleibol") == 0){
						sport_name = "volleyball"
					}
					else if(this.sport.localeCompare("Beisbol") == 0 || this.sport.localeCompare("Softbol") == 0){
						sport_name = "baseball"
					}
					else if(this.sport.localeCompare("Fútbol") == 0){
						sport_name = "soccer"
					}
					//MatchBased Sports
					else if(this.sport.localeCompare("Tenis de Campo") == 0 || this.sport.localeCompare("Tenis de Mesa") == 0){
						sport_name = "matchbased"
					}
					//Medal Based Sports
					else if(this.sport.localeCompare("Atletismo") == 0 || 
									this.sport.localeCompare("Judo") == 0 || 
									this.sport.localeCompare("Baile") == 0 || 
									this.sport.localeCompare("Halterofilia") == 0 || 
									this.sport.localeCompare("Campo Traviesa") == 0 ||
									this.sport.localeCompare("Lucha Olímpica") == 0 ||
									this.sport.localeCompare("Natación") == 0 ||
									this.sport.localeCompare("Porrismo") == 0 ||
									this.sport.localeCompare("Taekwondo") == 0){
						sport_name = "medalbased"
					}
					

					const stats_params = {'sport_name':sport_name,'athlete_id':this.athlete.id,'season_year':this.season}
					
					//First response is for the athlete season stats
					const response_1 = await this.getAthleteSeasonStats(stats_params)
					//Second response is for the aggregate athlete season stats
					const response_2 = await this.getAthleteAggregateSeasonStats(stats_params)

 					if(response_1 !== 'error' && response_2 !== 'error'){	
					
						//Assigns the correct Objects from the response depending on the sport name
						if(sport_name.localeCompare("basketball") == 0){
							for(let i = 0; i < this.athlete_stats_per_season.Basketball_Event_Season_Athlete_Statistics.length; i++){
								const statsObj =  this.athlete_stats_per_season.Basketball_Event_Season_Athlete_Statistics[i]
								this.statistics_per_season.push(statsObj)
								this.statistics_per_season[i].Event['event_date'] = this.formatedDate(statsObj.Event["event_date"])

							}
							this.aggregate_statistics_per_season.push(this.athlete_aggregate_stats_per_season.Basketball_Event_Season_Athlete_Statistics)
							this.buildHeadersList(sport_name)
						}

						else if(sport_name.localeCompare("baseball") == 0){
							for(let i = 0; i < this.athlete_stats_per_season.Baseball_Event_Season_Athlete_Statistics.length; i++){
								const statsObj =  this.athlete_stats_per_season.Baseball_Event_Season_Athlete_Statistics[i]
								this.statistics_per_season.push(statsObj)
								this.statistics_per_season[i].Event['event_date'] = this.formatedDate(statsObj.Event["event_date"])

							}
							this.aggregate_statistics_per_season.push(this.athlete_aggregate_stats_per_season.Baseball_Event_Season_Athlete_Statistics)
							this.buildHeadersList(sport_name)
						}
						else if(sport_name.localeCompare("volleyball") == 0){
							for(let i = 0; i < this.athlete_stats_per_season.Volleyball_Event_Season_Athlete_Statistics.length; i++){
								const statsObj =  this.athlete_stats_per_season.Volleyball_Event_Season_Athlete_Statistics[i]
								this.statistics_per_season.push(statsObj)
								this.statistics_per_season[i].Event['event_date'] = this.formatedDate(statsObj.Event["event_date"])

							}
							this.aggregate_statistics_per_season.push(this.athlete_aggregate_stats_per_season.Volleyball_Event_Season_Athlete_Statistics)
							this.buildHeadersList(sport_name)
						}
						else if(sport_name.localeCompare("soccer") == 0){
							for(let i = 0; i < this.athlete_stats_per_season.Soccer_Event_Season_Athlete_Statistics.length; i++){
								const statsObj =  this.athlete_stats_per_season.Soccer_Event_Season_Athlete_Statistics[i]
								this.statistics_per_season.push(statsObj)
								this.statistics_per_season[i].Event['event_date'] = this.formatedDate(statsObj.Event["event_date"])

							}
							this.aggregate_statistics_per_season.push(this.athlete_aggregate_stats_per_season.Soccer_Event_Season_Athlete_Statistics)
							this.buildHeadersList(sport_name)
						}
						else if(sport_name.localeCompare("matchbased") == 0){
							for(let i = 0; i < this.athlete_stats_per_season.Match_Based_Event_Season_Athlete_Statistics.length; i++){
								const statsObj =  this.athlete_stats_per_season.Match_Based_Event_Season_Athlete_Statistics[i]
								this.statistics_per_season.push(statsObj)
								this.statistics_per_season[i].Event['event_date'] = this.formatedDate(statsObj.Event["event_date"])

							}
							this.aggregate_statistics_per_season.push(this.athlete_aggregate_stats_per_season.Match_Based_Event_Season_Athlete_Statistics)
							this.buildHeadersList(sport_name)
						}
						else if(sport_name.localeCompare("medalbased") == 0){
							for(let i = 0; i < this.athlete_stats_per_season.Medal_Based_Event_Season_Athlete_Statistics.length; i++){
								const statsObj =  this.athlete_stats_per_season.Medal_Based_Event_Season_Athlete_Statistics[i]
								this.statistics_per_season.push(statsObj)
								this.statistics_per_season[i].Event['event_date'] = this.formatedDate(statsObj.Event["event_date"])

							}
							this.aggregate_statistics_per_season =this.athlete_aggregate_stats_per_season.Medal_Based_Event_Season_Athlete_Statistics							
							this.buildHeadersList(sport_name)
						}

						
					}
					this.fetchingAthleteStats = false
					this.fetchedData = true
				}
				
			},

			/**
			 * Builds and assigns the headers to be
			 * used on both data tables in the stats viewer
			 * tab depending on the sport_name given as a parameter.
			 * @param sport_name name of the sport of the athlete
			 */
			buildHeadersList(sport_name){
				if(sport_name.localeCompare("basketball") == 0){
					this.headers =	[
							{
								text:'Fecha del Evento',
								align: 'start',
								sortable: true,
								value:'Event.event_date'
							},
							{text: 'Asistencias', value: 'Event_Statistics.assists'},
							{text: 'Bloqueos', value: 'Event_Statistics.blocks'},
							{text: 'Intentos de Tiro de Campo', value: 'Event_Statistics.field_goal_attempt'},
							{text: 'Porcentaje de Tiro de Campo(%)', value: 'Event_Statistics.field_goal_percentage'},
							{text: 'Intentos de Tiro Libre', value: 'Event_Statistics.free_throw_attempt'},
							{text: 'Porcentaje de Tiro Libre(%)', value: 'Event_Statistics.free_throw_percentage'},
							{text: 'Puntos', value: 'Event_Statistics.points'},
							{text: 'Rebotes', value: 'Event_Statistics.rebounds'},
							{text: 'Robos', value: 'Event_Statistics.steals'},
							{text: 'Tiros de Campo Exitosos', value: 'Event_Statistics.successful_field_goal'},
							{text: 'Tiros Libres Exitosos', value: 'Event_Statistics.successful_free_throw'},
							{text: 'Tiros de Tres Puntos Exitosos', value: 'Event_Statistics.successful_three_point'},
							{text: 'Intentos de Tiro de Tres', value: 'Event_Statistics.three_point_attempt'},
							{text: 'Porcentaje de Tiro de Tres(%)', value: 'Event_Statistics.three_point_percentage'},
							{text: 'Perdidas de Balón', value: 'Event_Statistics.turnovers'},

					]
					this.headers_ = [
						{text: 'Asistencias', value: 'Event_Statistics.assists'},
						{text: 'Bloqueos', value: 'Event_Statistics.blocks'},
						{text: 'Intentos de Tiro de Campo', value: 'Event_Statistics.field_goal_attempt'},
						{text: 'Porcentaje de Tiro de Campo(%)', value: 'Event_Statistics.field_goal_percentage'},
						{text: 'Intentos de Tiro Libre', value: 'Event_Statistics.free_throw_attempt'},
						{text: 'Porcentaje de Tiro Libre(%)', value: 'Event_Statistics.free_throw_percentage'},
						{text: 'Puntos', value: 'Event_Statistics.points'},
						{text: 'Rebotes', value: 'Event_Statistics.rebounds'},
						{text: 'Robos', value: 'Event_Statistics.steals'},
						{text: 'Tiros de Campo Exitosos', value: 'Event_Statistics.successful_field_goal'},
						{text: 'Tiros Libres Exitosos', value: 'Event_Statistics.successful_free_throw'},
						{text: 'Tiros de Tres Puntos Exitosos', value: 'Event_Statistics.successful_three_point'},
						{text: 'Intentos de Tiro de Tres', value: 'Event_Statistics.three_point_attempt'},
						{text: 'Porcentaje de Tiro de Tres(%)', value: 'Event_Statistics.three_point_percentage'},
						{text: 'Perdidas de Balón', value: 'Event_Statistics.turnovers'},
					]
				}
				else if(sport_name.localeCompare("volleyball") == 0){
					this.headers =	[
						{
							text:'Fecha del Evento',
							align: 'start',
							sortable: true,
							value:'Event.event_date'
						},
						{text: 'Puntos de Ataque', value: 'Event_Statistics.kill_points'},
						{text: 'Errores de Ataque', value: 'Event_Statistics.attack_errors'},
						{text: 'Puntos de Bloqueo', value: 'Event_Statistics.blocking_points'},
						{text: 'Asistencias', value: 'Event_Statistics.assists'},
						{text: 'Servicio Directo', value: 'Event_Statistics.aces'},
						{text: 'Errores de Servicio', value: 'Event_Statistics.service_errors'},
						{text: 'Recepciones', value: 'Event_Statistics.digs'},
						{text: 'Bloqueo', value: 'Event_Statistics.blocks'},
						{text: 'Errores de Bloqueo', value: 'Event_Statistics.blocking_errors'},
						{text: 'Errores de Recepción', value: 'Event_Statistics.reception_errors'}
							

					]
					this.headers_ = [
						{text: 'Puntos de Ataque', value: 'Event_Statistics.kill_points'},
						{text: 'Errores de Ataque', value: 'Event_Statistics.attack_errors'},
						{text: 'Puntos de Bloqueo', value: 'Event_Statistics.blocking_points'},
						{text: 'Asistencias', value: 'Event_Statistics.assists'},
						{text: 'Servicio Directo', value: 'Event_Statistics.aces'},
						{text: 'Errores de Servicio', value: 'Event_Statistics.service_errors'},
						{text: 'Recepciones', value: 'Event_Statistics.digs'},
						{text: 'Bloqueo', value: 'Event_Statistics.blocks'},
						{text: 'Errores de Bloqueo', value: 'Event_Statistics.blocking_errors'},
						{text: 'Errores de Recepción', value: 'Event_Statistics.reception_errors'}							
						
					]
				}
				else if(sport_name.localeCompare("soccer") == 0){
					this.headers =	[
						{
							text:'Fecha del Evento',
							align: 'start',
							sortable: true,
							value:'Event.event_date'
						},
						{text: 'Intentos de Gol', value: 'Event_Statistics.goal_attempts'},
						{text: 'Asistencias', value: 'Event_Statistics.assists'},
						{text: 'Faltas', value: 'Event_Statistics.fouls'},
						{text: 'Tarjetas', value: 'Event_Statistics.cards'},
						{text: 'Goles Exitosos', value: 'Event_Statistics.successful_goals'},
						{text: 'Entradas', value: 'Event_Statistics.tackles'}
							

					]
					this.headers_ = [
						{text: 'Intentos de Gol', value: 'Event_Statistics.goal_attempts'},
						{text: 'Asistencias', value: 'Event_Statistics.assists'},
						{text: 'Faltas', value: 'Event_Statistics.fouls'},
						{text: 'Tarjetas', value: 'Event_Statistics.cards'},
						{text: 'Goles Exitosos', value: 'Event_Statistics.successful_goals'},
						{text: 'Entradas', value: 'Event_Statistics.tackles'}
					]
				}
				else if(sport_name.localeCompare("baseball") == 0){
					this.headers =	[
						{
							text:'Fecha del Evento',
							align: 'start',
							sortable: true,
							value:'Event.event_date'
						},
						{text: 'Turnos al Bate', value: 'Event_Statistics.at_bats'},
						{text: 'Carreras', value: 'Event_Statistics.runs'},
						{text: 'Hits', value: 'Event_Statistics.hits'},
						{text: 'Carreras Empujadas', value: 'Event_Statistics.runs_batted_in'},
						{text: 'Bases Por Bolas', value: 'Event_Statistics.base_on_balls'},
						{text: 'Ponches', value: 'Event_Statistics.strikeouts'},
						{text: 'Dejados en Base', value: 'Event_Statistics.left_on_base'}
							

					]
					this.headers_ = [
						{text: 'Turnos al Bate', value: 'Event_Statistics.at_bats'},
						{text: 'Carreras', value: 'Event_Statistics.runs'},
						{text: 'Hits', value: 'Event_Statistics.hits'},
						{text: 'Carreras Empujadas', value: 'Event_Statistics.runs_batted_in'},
						{text: 'Bases Por Bolas', value: 'Event_Statistics.base_on_balls'},
						{text: 'Ponches', value: 'Event_Statistics.strikeouts'},
						{text: 'Dejados en Base', value: 'Event_Statistics.left_on_base'}				
					]
				}
				else if(sport_name.localeCompare("matchbased") == 0){
					this.headers =	[
						{
							text:'Fecha del Evento',
							align: 'start',
							sortable: true,
							value:'Event.event_date'
						},
						{text: 'Categoría', value: 'Event.category_name'},
						{text: 'Partidas Jugadas', value: 'Event_Statistics.matches_played'},
						{text: 'Partidas Ganadas', value: 'Event_Statistics.matches_won'}

					]
					this.headers_ = [
						{text: 'Categoría', value: 'Event_Statistics.category_name'},
						{text: 'Partidas Jugadas', value: 'Event_Statistics.matches_played'},
						{text: 'Partidas Ganadas', value: 'Event_Statistics.matches_won'}					
					]
				}
				else if(sport_name.localeCompare("medalbased") == 0){
					this.headers =	[
						{
							text:'Fecha del Evento',
							align: 'start',
							sortable: true,
							value:'Event.event_date'
						},
						{text: 'Categoría', value: 'Event.category_name'},
						{text: 'Tipo de Medalla', value: 'Event_Statistics.type_of_medal'}
					

					]
					this.headers_ = [
						{text: 'Categoría', value: 'Event_Statistics.category_name'},
						{text: 'Tipo de Medalla', value: 'Event_Statistics.type_of_medal'},
						{text: 'Númbero de Medallas', value: 'Event_Statistics.medals_earned'}					
					]
				}
				
			}
		},

		computed: {
			...mapGetters({
				athlete:"athletes/athlete",
				athlete_stats_per_season:"athletes/athlete_stats_per_season",
				athlete_aggregate_stats_per_season:"athletes/athlete_aggregate_stats_per_season"
			})
		},

		

		
}
</script>

<style lang="scss" scoped>
::v-deep .v-data-table th {
  font-size: 1rem;
}

::v-deep .v-data-table td {
  font-size: 1rem;
}
</style>

