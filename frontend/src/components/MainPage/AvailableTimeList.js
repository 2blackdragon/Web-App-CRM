import "../../styles/AvailableTimeList.css"
import api from "../Api"

function AvailableTimeList (props) {

    const master_id = props.master_id;
    const time_data = props.time_data;
    const datetime_for_db = props.datetime_for_db;

    const post_record = async (event) => {
        event.preventDefault();
        await api.post("/add_record", {"master_id": master_id, "client_id": 3, "record_datetime": datetime_for_db});
        document.location.reload();
    }

    return (
        <div className="time_list">
            {time_data.map((available_time) => {
                return (
                    <button onClick={post_record} className="time_btn">{available_time} </button>
                )
            })}
        </div>
    )
}

export default AvailableTimeList;