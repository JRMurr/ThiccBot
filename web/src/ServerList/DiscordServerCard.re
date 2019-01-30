let component = ReasonReact.statelessComponent("DiscordServerCard");
open ServerTypes;
let make = (~server: discordServer, _children) => {
  ...component, /* spread the template's other defaults into here  */
  render: _self => {
    /* <div> (ReasonReact.string(server.name)) ((server.id |> string_of_int |> ReasonReact.string)) </div> */
    <div className="card border-primary mb-3">
      /* <div className="card-header">(ReasonReact.string("Header"))</div> */
        <div className="card-body">
            <h4 className="card-title"> {ReasonReact.string(server.name)} </h4>
          </div>
          /* <p className="card-text">(ReasonReact.string("Some quick example text to build on the card title and make up the bulk of the card's content."))</p> */
      </div>;
  },
};