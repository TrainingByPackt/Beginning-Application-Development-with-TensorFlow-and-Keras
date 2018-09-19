<template>
<div id="app">
    <div>
        <el-col>
            <el-col :span="4"></el-col>
            <el-col :span="16">
                <el-row>
                    <el-col :span="20">
                        <h2>Cryptonic</h2>
                        
                    </el-col>
                    <el-col :span="4">
        
                        <el-tooltip class="item" effect="dark" v-bind:content=" component_message " placement="bottom-end">
                             <span style="margin-top: 30%; margin-right: 2%; float: right;" v-bind:class="{ alert_red: alertError, alert_green: alertNoError }"></span>
                        </el-tooltip>
            
                    </el-col>
                </el-row>
                <el-row>
                    <el-col>
                        <p>
                            Welcome to <u>cryptonic</u>! Cryptonic is an application that predicts the next few days of Bitcoin prices usign a Deep Learning model. The current model is designed using a recurrent neural network (or, better, its Long Short Term Memory variant) and trained with historic Bitcoin data.
                        </p>
                        <p>
                            More specifically, the model looks at a sequence of N days and identifies patterns that happen within that period of time. It then looks at the next sequence of N days to identify new patterns, but now also looking at their relationship with previous periods. Periods that come later can tap into patterns observed earlier. The predictions shown in the plot below are created based on patterns observed in all previous periods.
                        </p>
                        <p>
                            This simple model has a root mean squared error of <b>${{ rmse }}</b> US dollars and a mean averaged percentage error of <b>{{ mape }}%</b>.
                        </p>
                    </el-col>
                </el-row>
                <el-row>
                    <div id="chart"></div>
                </el-row>
                <el-row>
                    <el-col>
                        <p>
                            This application was created for educational purposes. It is part of the book "Beginning Application Development with TensorFlow" (Packt, 2018) by <a href="https://luiscapelo.info">Luis Capelo</a>.
                        </p>
                        <p>
                            Original data comes from <a href="https://coinmarketcap.com/">CoinMarketCap</a>.
                        </p>
                        {{ now | moment('h:mm:ss a') }} (<i>local time</i>)
                    </el-col>
                </el-row>
            
            </el-col>
            <el-col :span="4">

                

            </el-col>
        </el-col>
    </div>
</div>

</template>

<script>

export default {
    data () {
        return {
            now: this.$moment(new Date()),
            loading: true,
            base_url: '',
            alertError: false,
            rmse: 0,
            mape: 0,
            chart_historic_data: {
                'date': [],
                'observation': []
            },
            chart_prediction_data: {
                'date': [],
                'prediction': []
            },
            alertNoError: true,
            component_message: 'API not accessible.',
            currentDate: new Date()
        }
    },
    methods: {
        platformClass (platform) {
            return 'platform-background-' + platform
        },
        getStatus () {
            console.log('[Cryptonic components]: Checking component status ...')

            var self = this
            var query_url = `${self.base_url}/status`

            self.component_status = []
            self.errored_components = []
            this.$http.get(query_url).then(
                function(response) {
                    if (response.data.success) { 
                        self.component_message = 'API accessible.'
                        self.alertError = false
                        self.alertNoError = true
                        self.rmse = response.data.model.error_rates.rmse
                        self.mape = response.data.model.error_rates.mape
                    } else {
                        self.component_message = 'API not accessible.'
                        self.alertError = true
                        self.alertNoError = false
                    }
                }, 
                function(response) {
                    console.log('[Cryptonic components] Found error making request.')
                    self.component_message = 'API not accessible.'
                    self.alertError = true
                    self.alertNoError = false
                })
        },
        getHistoricalData (callback) {
            console.log('[Historic API] Fetching historic data.')

            var self = this
            var url = `${self.base_url}/historic`
            this.$http.get(url).then(
                function (response) {
                    if (response.data.success) {
                        self.chart_historic_data = {
                            'date': [],
                            'observation': []
                        }
                        response.data['result'].forEach(function(x) {
                            self.chart_historic_data['date'].push(x['date'])
                            self.chart_historic_data['observation'].push(x['close'])
                        })
                        callback()
                    } else {
                        self.chart_historic_data = false
                    }
                }, function (response) {
                    console.log('[Historic API] Failed to fetch historic data.')
                }
            )

            console.log('[Historic API] Done.')
        },
        getPredictionData (callback) {
            console.log('[Prediction API] Fetching prediction data.')

            var self = this
            var url = `${self.base_url}/predict`
            this.$http.get(url).then(
                function (response) {
                    self.chart_prediction_data = {
                        'date': [],
                        'prediction': []
                    }
                    if (response.data.success) {
                        response.data['result'].forEach(function(x) {
                            self.chart_prediction_data['date'].push(x['date'])
                            self.chart_prediction_data['prediction'].push(x['prediction'])
                        })
                        callback()
                    } else {
                        self.chart_prediction_data = false
                    }
                }, function (response) {
                    console.log('[Prediction API] Failed to fetch prediction data data.')
                }
            )
            console.log('[Predictions API] Done.')
        },
        fillMissingData(callback) {
            console.log('[Charting] Filling missing data.')

            var historic_filler = []
            for (var i = 0; i < this.chart_prediction_data['prediction'].length; i++) {
                historic_filler.push(null)
            }

            var predictions_filler = []
            for (var i = 0; i < this.chart_historic_data['observation'].length; i++) {
                predictions_filler.push(null)
            }

            this.chart_data = {
                x: this.chart_prediction_data['date'].concat(this.chart_historic_data['date']), 
                observed: historic_filler.concat(this.chart_historic_data['observation']),
                predicted: predictions_filler.concat(this.chart_prediction_data['prediction']).reverse()
            }

            console.log('[Charting] Done.')
            callback()
        },
        createChart(data) {
            console.log('[Charting] Generating chart.')

            var self = this
            this.$c3.generate({
                data: {
                    x: 'x', 
                    json: self.chart_data,
                    types: {
                        observed: 'area',
                        predicted: 'area'
                    },
                    colors: {
                        observed: '#95a5a6',
                        predicted: '#e74c3c'
                    }
                },
                point: {
                    show: true
                },
                grid: {
                    x: {
                        show: true
                    }
                },
                axis: {
                    x: {
                        type: 'timeseries',
                        tick: {
                            format: '%Y-%m-%d',
                        }
                    },
                    y: {
                        tick: {
                            culling: {
                                max: 4
                            }
                        }
                    }
                }
            })
        }
    },
    mounted() {
        var self = this
        this.getStatus()
        this.loading = false

        setInterval(function () {
            this.getStatus()
        }.bind(this), 1000 * 60)

        setInterval(function () {
            this.now = this.$moment(new Date())
        }.bind(this), 1000 * 1)

        this.getHistoricalData(function (x) {
            self.getPredictionData(function (x) {
                self.fillMissingData(function (x) {
                    self.createChart()
                })
            })
        })

    }
}
</script>


<style>
    .el-card a {
        color: inherit;
        text-decoration: none;
    }
    .el-col {
        padding: 10px 0px 10px 10px;
    }
    .el-tag {
        font-size: 10px;
    }
    .platform-background-facebook {
        background: #3b5998;
        height: 100px;
        width: 10px;
    }
    .platform-background-twitter {
        background: #1DA1F2;
        height: 100px;
        width: 10px;
    }
    .platform-background-tumblr {
        background: #35465c;
        height: 100px;
        width: 10px;
    }
    .platform-background-linkedin {
        background: #0077B5;
        height: 100px;
        width: 10px;
    }
    .period-divider {
        color: #cccccc;
    }
    .period-divider hr {
        border-color: rgba(111,111,111,0.1) transparent;
        border-width: 0.1em;
        border-style: solid;
    }
    .credits {
        position: relative;
        bottom: 0;
    }
    .no-left-margin {
        margin-left: 0px !important;
    }
    .grid-content {
        font-size: 10px;
        border-radius: 4px;
        min-height: 36px;
        overflow: hidden;
        color: #999;
    }
    .results-content { 
        padding-left: 0px;
    }
    .sbx-google {
        width: 100%;
    }
    .centered {
        position: fixed;
        top: 50%;
        left: 50%;
        margin-top: -50px;
        margin-left: -100px;
        padding-left: 3.6em;
        padding-top: 10em;
    }
    .bottom {
        margin-top: 13px;
        line-height: 12px;
    }

    .button {
        padding: 0;
        float: right;
    }

    .image {
        width: 100%;
        display: block;
    }

    .clearfix:before,
    .clearfix:after {
        display: table;
        content: "";
    }
    .clearfix:after {
        clear: both
    }
    .c3-line {
        stroke-width: 2px;
    }
</style>