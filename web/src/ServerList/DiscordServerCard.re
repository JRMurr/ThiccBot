let component = ReasonReact.statelessComponent("DiscordServerCard");
open ServerTypes;
let make = (~server: discordServer, _children) => {
  let click = (_event, _self) => {
    ReasonReact.Router.push("/server/" ++ server.id);
  };
  {
    ...component, /* spread the template's other defaults into here  */
    render: self => {
      /* <div> (ReasonReact.string(server.name)) ((server.id |> string_of_int |> ReasonReact.string)) </div> */
      <div className="card border-primary mb-3" onClick={self.handle(click)}>
        /* <div className="card-header">(ReasonReact.string("Header"))</div> */

          <div className="card-body">
            <h4 className="card-title">
              {ReasonReact.string(server.name ++ " id: " ++ server.id)}
            </h4>
          </div>
        </div>;
        /* <p className="card-text">(ReasonReact.string("Some quick example text to build on the card title and make up the bulk of the card's content."))</p> */
    },
  };
};