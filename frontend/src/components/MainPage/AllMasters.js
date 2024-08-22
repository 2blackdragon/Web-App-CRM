import api from "../Api"
import { useEffect, useState } from "react"
import MasterAvailableDatetime from "./MasterAvailableDatetime"

function AllMasters () {
    const fetch_all_available_datetime = async () => {
        const response = await api.get("/");
        setAllAvailableDatetimes(response.data);
    }

    const [allAvailableDatetime, setAllAvailableDatetimes] = useState([]);
    useEffect( () => {
        fetch_all_available_datetime();
    }, []);

    return (
            <div className="body_container">
                <div className="all_available_records">
                    <h1>Запись на прием к косметологу</h1>
                    <div>
                        {allAvailableDatetime.map((element) => {
                            const modify_element = JSON.parse(element);
                            return (
                                <MasterAvailableDatetime master_data={modify_element}/>
                            )
                        })}
                    </div>
                </div>
            </div>
    )
}

export default AllMasters;