"use client"
import { useState, useEffect } from "react";

import {
  Card, 
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
  CardAction
} from "@/components/ui/card";

interface User{
  user_id: number,
  name: string,
  phone_number: string,
  email: string
}


export default function Home() {
    
    const [users, setUsers] = useState([]);
    
    useEffect(() => {
        fetch("http://127.0.0.1:8000/sim/")
            .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
            })
            .then(data => setUsers(data))
            .catch(error => console.error("Fetch error:", error));
    }, []);
    
    return (
      
      <main>
        <div className= "grid grid-cols-2 gap-8">
          {users.map(user => (
            <Card key={user.user_id}>
              <CardHeader>
                <div>
                  <CardTitle>{user.name}</CardTitle>
                  <CardContent>Phone: {user.phone_number}</CardContent>
                  <CardContent>Email: {user.email}</CardContent>
                </div>
              </CardHeader>

            </Card>
          ))}

        </div>
      </main>

    );
}