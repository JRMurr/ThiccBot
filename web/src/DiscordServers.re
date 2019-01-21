/* The new stdlib additions */
open Belt;

type discordServers = {
  admin_role: option(int),
  command_prefixes: option(array(string)),
  id: int,
  name: string
};

type state =
  | Loading
  | Error
  | Loaded(array(discordServers));

type action =
  | ServerFetch
  | ServersFetches(array(discordServers))
  | ServersFailedToFetch;


module API = {
  /* open Json.Decode; */
  let decodeServer = json =>
    Json.Decode.{
      admin_role: json |> field("admin_role", optional(int)),
      command_prefixes: json |> field("command_prefixes", optional(array(string))),
      id:  json |> field("id", int),
      name: json |> field("name", string)
    };
  
  let decodeAllServers = Json.Decode.array(decodeServer)

  let getServers = () =>
    Js.Promise.(
      Fetch.fetch("api/servers")
      |> then_(Fetch.Response.json)
      |> then_(json => decodeAllServers(json) |> resolve)
    );
};

let component = ReasonReact.reducerComponent("FetchExample");

let make = _children => {
  ...component,
  initialState: _state => Loading,
  reducer: (action, _state) =>
    switch (action) {
    | ServerFetch =>
      ReasonReact.UpdateWithSideEffects(
        Loading,
        (
          self => {
            let _ = API.getServers()
            |> Js.Promise.then_(results => {
                   self.send(ServersFetches(results))
                   Js.Promise.resolve();
                 })
            |> Js.Promise.catch(_err => Js.Promise.resolve(self.send(ServersFailedToFetch)));
            ();
          }
        ),
      )
    | ServersFetches(servers) => ReasonReact.Update(Loaded(servers))
    | ServersFailedToFetch => ReasonReact.Update(Error)
    },
  didMount: self => self.send(ServerFetch),
  render: self =>
    switch (self.state) {
    | Error => <div> (ReasonReact.string("An error occurred!")) </div>
    | Loading => <div> (ReasonReact.string("Poop...")) </div>
    | Loaded(servers) =>
      <div>
        <h1> (ReasonReact.string("Servers")) </h1>
        <ul>
          (
            Array.map(servers, (server =>
              <li key=server.name> (server.name |> ReasonReact.string) </li>
            ))
            |> ReasonReact.array
          )
        </ul>
      </div>
    },
};