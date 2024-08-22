import "../../styles/MasterAvailableDatetime.css"
import AvailableTimeList from "./AvailableTimeList"


function convert_master_data (master_available_datetime) {
    const DAYS_OF_WEEK = ["вс", "пн", "вт", "ср", "чт", "пт", "сб"];
    const MONTH = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", 
                   "августа", "сентября", "октября", "ноября", "декабря"];
    const result = new Map();
    for (let i = 0; i < master_available_datetime.length; i++){
        const datetime = new Date(master_available_datetime[i])
        const day = datetime.getDate() + " " + MONTH[datetime.getMonth()] + " " + DAYS_OF_WEEK[datetime.getDay()]
        if (result.has(day)){
            const prev = result.get(day);
            prev.push(datetime.getHours() + ":" + datetime.getMinutes());
            result.set(day, prev)
        }
        else{
            const el = []
            el.push(datetime.getHours() + ":" + datetime.getMinutes())
            result.set(day, el)
        }
    }

    const result_set = [];
    var i = 0;
    for (var [key, value] of result){
        const el = new Map();
        el.set("day", key);
        el.set("time_list", value)
        el.set("datetime_for_db", master_available_datetime[i])
        result_set.push(el);
        i = i + 1;
    }
    
    return result_set;
}


function MasterAvailableDatetime (props) {
    const master_id = props.master_data.master_id
    const master_available_datetime = convert_master_data(props.master_data.master_available_datetime);

    return (
        <div className="master_data">
            <h3>{props.master_data.master_fullname}</h3>
            {master_available_datetime.map((element) => {
                const number = element.get("day").split(" ")[0];
                const month = element.get("day").split(" ")[1];
                const weekday = element.get("day").split(" ")[2];

                const time_data = element.get("time_list");

                const datetime_for_db = element.get("datetime_for_db");

                return (
                    <div className="day_and_time">
                        <div className="day">
                            <div className="number_and_weekday">
                                <div className="number">{number}</div>
                                <div className="weekday">{weekday}</div>
                            </div>
                            <div className="month">{month}</div>
                        </div>

                        <div className="time">
                            <AvailableTimeList master_id={master_id} 
                                               time_data={time_data} 
                                               datetime_for_db={datetime_for_db}
                                                />
                        </div>
                    </div>
                )
            })}
        </div>
    )
}

export default MasterAvailableDatetime;