let component = ReasonReact.statelessComponent("DiscordServerCard");

let make = (~name: string, _children) => {
  ...component, /* spread the template's other defaults into here  */
  render: _self => <div> {ReasonReact.string(name)} </div>
};