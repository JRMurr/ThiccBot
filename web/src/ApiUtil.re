let getJson = (~route: string, ~decoder, ()) => 
    Js.Promise.(
        Fetch.fetch(route)
        |> then_(Fetch.Response.json)
        |> then_(json => decoder(json) |> resolve)
    );

